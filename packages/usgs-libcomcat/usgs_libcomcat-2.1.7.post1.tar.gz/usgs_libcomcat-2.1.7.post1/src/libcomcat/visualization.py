from datetime import timedelta
import numpy as np
import pandas as pd
import pathlib
import math
import json
import matplotlib.pyplot as plt
from esi_utils_rupture.quad_rupture import QuadRupture
from esi_utils_rupture.origin import Origin
from obspy.imaging.beachball import beach
from esi_utils_colors.cpalette import ColorPalette
from io import StringIO
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

PRODUCT_COLORS = {
    "finite-fault": "#C5CAF5",
    "ground-failure": "#A2F5EF",
    "losspager": "#F6D5E4",
    "moment-tensor": "#C9DCF5",
    "origin": "#CEF3B4",
    "shakemap": "#FFEFD5",
    "dyfi": "#7D7D7D",
    "oaf": "#E6B17E",
    "phase-data": "#F5B69C",
    "default": "#72DCB7",
    "focal-mechanism": "#EC7063",
}


class Timeline:
    def __init__(self, max_time, dataframe, event_details, timeline_format):
        if max_time > 5760:
            self.max_time = 5760

        else:
            self.max_time = max_time

        self.dataframe = dataframe

        self.event_details = event_details

        self.timeline_format = timeline_format

        self.finite_fault_count = 0

    def create_timeline(self):
        self.shortened_history = self.dataframe.loc[
            (self.dataframe["Product"] != "dyfi")
            & (self.dataframe["Product"] != "phase-data")
            & (self.dataframe["Elapsed (min)"] < self.max_time)
            & (self.dataframe["Elapsed (min)"] >= 0)
            & (self.dataframe["Product"] != "oaf")
        ]
        # not including dyfi or oaf products in timeline, not including
        # anything done 4 days later

        if len(self.shortened_history) == 0:
            return

        max_time = float(self.shortened_history.iloc[-1]["Elapsed (min)"])

        self.dyfi_frame = self.dataframe[self.dataframe["Product"] == "dyfi"]
        self.dyfi_frame = self.dyfi_frame.loc[
            (
                self.dyfi_frame["Description"]
                .str.split("|")
                .str[1]
                .str.split("# ")
                .str[1]
                != "0"
            )
            & (self.dyfi_frame["Elapsed (min)"] < max_time)
            & (self.dyfi_frame["Elapsed (min)"] >= 0)
        ]

        self.oaf_frame = self.dataframe[self.dataframe["Product"] == "oaf"]
        self.oaf_frame = self.oaf_frame.loc[
            (self.oaf_frame["Elapsed (min)"] < max_time)
            & (self.oaf_frame["Elapsed (min)"] >= 0)
        ]

        if self.shortened_history.empty:
            print("No data available to create a timeline.")
            return

        self.determine_spacing()

        self.create_plot()

        self.shortened_history = pd.concat(
            [self.shortened_history, self.dyfi_frame, self.oaf_frame]
        )

        self.shortened_history = self.shortened_history.sort_values(by="Elapsed (min)")

        self.create_boxes()

        return self.figure

    def determine_spacing(self):
        """
        Determines the space dedicated to each time period.
        """

        # calculates how many instances are present in each time block
        bins = [-1, 60, 180, 240, 420, 600, 1200, 1440, 5760]

        total = len(self.shortened_history)

        bins_hrs = pd.cut(self.shortened_history["Elapsed (min)"], bins=bins)
        hrs_counts = bins_hrs.value_counts()

        hr_1 = hrs_counts[0]
        hr_2_3 = hrs_counts[61]
        hr_4 = hrs_counts[181]
        hr_4_7 = hrs_counts[241]
        hr_7_10 = hrs_counts[421]
        hr_10_20 = hrs_counts[601]
        hr_20_24 = hrs_counts[1201]
        hr_24 = hrs_counts[1441]

        # calculates how much of the timeline should be dedicated to each time block
        self.DEFAULT_1HR_SPACE = hr_1 / total
        self.DEFAULT_2_3_SPACE = hr_2_3 / total
        self.DEFAULT_4HR_SPACE = hr_4 / total
        self.DEFAULT_4_7_SPACE = hr_4_7 / total
        self.DEFAULT_7_10_SPACE = hr_7_10 / total
        self.DEFAULT_10_20_SPACE = hr_10_20 / total
        self.DEFAULT_20_24_SPACE = hr_20_24 / total
        self.DEFAULT_24_SPACE = hr_24 / total

        self.elapsed_space = {
            "1hr": self.DEFAULT_1HR_SPACE,
            "2-3hr": self.DEFAULT_1HR_SPACE + self.DEFAULT_2_3_SPACE,
            "4hr": self.DEFAULT_1HR_SPACE
            + self.DEFAULT_2_3_SPACE
            + self.DEFAULT_4HR_SPACE,
            "4-7hr": self.DEFAULT_1HR_SPACE
            + self.DEFAULT_2_3_SPACE
            + self.DEFAULT_4HR_SPACE
            + self.DEFAULT_4_7_SPACE,
            "7-10hr": self.DEFAULT_1HR_SPACE
            + self.DEFAULT_2_3_SPACE
            + self.DEFAULT_4HR_SPACE
            + self.DEFAULT_4_7_SPACE
            + self.DEFAULT_7_10_SPACE,
            "10-20hr": self.DEFAULT_1HR_SPACE
            + self.DEFAULT_2_3_SPACE
            + self.DEFAULT_4HR_SPACE
            + self.DEFAULT_4_7_SPACE
            + self.DEFAULT_7_10_SPACE
            + self.DEFAULT_10_20_SPACE,
            "20-24hr": self.DEFAULT_1HR_SPACE
            + self.DEFAULT_2_3_SPACE
            + self.DEFAULT_4HR_SPACE
            + self.DEFAULT_4_7_SPACE
            + self.DEFAULT_7_10_SPACE
            + self.DEFAULT_10_20_SPACE
            + self.DEFAULT_20_24_SPACE,
            "24hr+": self.DEFAULT_1HR_SPACE
            + self.DEFAULT_2_3_SPACE
            + self.DEFAULT_4HR_SPACE
            + self.DEFAULT_4_7_SPACE
            + self.DEFAULT_7_10_SPACE
            + self.DEFAULT_10_20_SPACE
            + self.DEFAULT_20_24_SPACE
            + self.DEFAULT_24_SPACE,
        }

    def create_plot(self):
        """Creates the plot."""

        self.plot_arrow()

        self.plot_times()

        if len(self.dyfi_frame) > 0:
            self.plot_dyfi()

        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["right"].set_visible(False)

        self.plot_legend()

        # information for the title, and plotting the title
        eventID = f"Event ID: {self.event_details.id}"
        location = f"Location: {self.event_details.location}"
        day = f"Day: {str(self.event_details.time).split()[0]}"
        mag = f"Magnitude: {self.event_details.magnitude}"

        self.ax.set_title(
            f"{eventID}     {location}     {day}     {mag}",
            y=1.05,
        )

    def create_boxes(self):
        """Creates the product boxes on the timeline

        Returns:
            figure (figure): Returns the figure object of the timeline
        """

        top = 1
        # top controls whether an instance is on the top or bottom of the timeline
        top_count = 0
        # top_count and other_count determine which level an instance in on on
        # the top or bottom of the timeline
        other_count = 0

        # tracking dyfi and oaf information
        dyfi_x = []
        dyfi_y = []
        dyfi = False

        oaf = False
        self.first_oaf = True

        # plots the instances
        for idx, row in self.shortened_history.iterrows():

            ptype = row["Product"]
            elapsed_min = row["Elapsed (min)"]
            elapsed = elapsed_min / 60.0
            psource = row["Product Source"]

            product_row = row["Description"].split("|")

            # determining the product summary/statement
            # product statement controls how much extra space the text box has
            # to add minibits
            # product summary controls what will be put in the minibit if it is
            # text
            if ptype == "ground-failure":
                instance_1 = product_row[-1].split("# ")
                instance_2 = product_row[-2].split("# ")

                if instance_1[0] == "Landslide Alert":
                    landslide = instance_1[1]
                    liquefaction = instance_2[1]

                else:
                    landslide = instance_2[1]
                    liquefaction = instance_1[1]

                if landslide != "pending" and liquefaction != "pending":
                    product_statement = "\n"
                else:
                    product_statement = ""

            elif ptype == "dyfi":
                product_statement = ""

            elif ptype == "oaf":
                percentages, occurrences = self.oaf_data()

                if percentages != -1:
                    mag = math.floor(self.event_details.magnitude) - 1

                    if mag < 3:
                        mag == 3

                    mag_str = f"M{mag}+"

                    percent = percentages[mag - 2]

                    product_statement = ""

                    product_summary = f"{mag_str}: {percent}"
                else:
                    product_summary = ""

            else:
                product_summary = product_row[0].split("# ")[1]

                product_statement = ""

                if ptype == "origin":
                    origin = product_row[-4].split("# ")[1]
                    product_summary = f"{origin} {product_summary}"
                elif ptype == "finite-fault":
                    product_statement = "\n"

                elif ptype == "moment-tensor":

                    strike = int(product_row[-3].split("# ")[1])
                    dip = int(product_row[-2].split("# ")[1])
                    rake = int(product_row[-1].split("# ")[1])

                    beachball_stats = [strike, dip, rake]

                    magnitude = product_row[1].split("# ")[1]

                    product_statement = f"{product_summary}  {magnitude} \n"

            # oaf and losspager have weird capitalization
            type = ptype.capitalize()
            if type == "Oaf":
                type = "OAF"
            if type == "Losspager":
                type = "PAGER"
            source = psource.upper()

            # determines the statement and horizontal location of text boxes
            if elapsed_min <= 60:
                elapsed = elapsed * self.DEFAULT_1HR_SPACE * self.arrow_length
                time = f"{(elapsed_min):.1f} min:"
            elif elapsed_min < 180:
                elapsed = (
                    (elapsed_min - 60)
                    / 120
                    * self.arrow_length
                    * self.DEFAULT_2_3_SPACE
                    + self.DEFAULT_1HR_SPACE * self.arrow_length
                )
                time = f"{(elapsed_min / 60):.1f} hrs:"
            elif elapsed_min < 240:
                elapsed = (
                    elapsed_min - 180
                ) / 60 * self.arrow_length * self.DEFAULT_4HR_SPACE + (
                    self.elapsed_space["2-3hr"]
                ) * self.arrow_length
                time = f"{(elapsed_min / 60):.1f} hrs:"
            elif elapsed_min < 420:
                elapsed = self.arrow_length * (self.DEFAULT_4_7_SPACE) * (
                    elapsed_min - 240
                ) / 180 + self.arrow_length * (self.elapsed_space["4hr"])
                time = f"{(elapsed_min / 60):.1f} hrs:"
            elif elapsed_min < 600:
                elapsed = self.arrow_length * (self.DEFAULT_7_10_SPACE) * (
                    elapsed_min - 420
                ) / 180 + self.arrow_length * (self.elapsed_space["4-7hr"])
                time = f"{(elapsed_min / 60):.1f} hrs:"
            elif elapsed_min < 1200:
                elapsed = self.arrow_length * (self.DEFAULT_10_20_SPACE) * (
                    elapsed_min - 600
                ) / 600 + self.arrow_length * (self.elapsed_space["7-10hr"])
                time = f"{(elapsed_min / 60):.1f} hrs:"
            elif elapsed_min < 1440:
                elapsed = self.arrow_length * (self.DEFAULT_20_24_SPACE) * (
                    elapsed_min - 1200
                ) / 240 + self.arrow_length * (self.elapsed_space["10-20hr"])
                time = f"{(elapsed_min / 60):.1f} hrs:"
            else:
                elapsed = self.arrow_length * (self.DEFAULT_24_SPACE) * np.log(
                    (elapsed_min - 1440) / 60 / self.arrow_length + 1
                ) + self.arrow_length * (self.elapsed_space["20-24hr"])
                time = f"{(elapsed_min / 1440):.1f} d:"

            if product_summary == "unknown nan" and ptype == "origin":
                self.deleted(
                    "red",
                    elapsed,
                    f"{time} {source} \n {ptype.capitalize()} \n Deleted",
                )

                continue

            pstring = f"{time} {source} \n {type} \n {product_statement}"

            if (ptype != "dyfi" and ptype != "oaf") or (
                ptype == "oaf" and self.first_oaf
            ):

                if ptype == "oaf" and self.first_oaf:
                    self.first_oaf = False
                    # only first oaf is plotted

                # determines vertical distance of textbox, 8 levels, 4 on
                # top and 4 on bottom
                if top:
                    if top_count % 4 == 0:
                        ytext = self.arrow_middle + (self.arrow_width * 5)
                    elif top_count % 4 == 1:
                        ytext = self.arrow_middle + (self.arrow_width * 10)
                    elif top_count % 4 == 2:
                        ytext = self.arrow_middle + (self.arrow_width * 15)
                    else:
                        ytext = self.arrow_middle + (self.arrow_width * 20)
                    fontsize = 10
                    if (
                        ptype == "moment-tensor"
                        or ptype == "ground-failure"
                        or ptype == "finite-fault"
                    ):
                        fontsize = 9
                    top = 0
                    top_count += 1
                    vertical_dist = self.arrow_middle + self.arrow_width / 2
                    plt.vlines(elapsed, vertical_dist, ytext, colors="black")
                else:
                    if other_count % 4 == 0:
                        ytext = self.arrow_middle - (self.arrow_width * 6)
                    elif other_count % 4 == 1:
                        ytext = self.arrow_middle - (self.arrow_width * 11)
                    elif other_count % 4 == 2:
                        ytext = self.arrow_middle - (self.arrow_width * 16)
                    else:
                        ytext = self.arrow_middle - (self.arrow_width * 21)
                    fontsize = 10
                    if (
                        ptype == "moment-tensor"
                        or ptype == "ground-failure"
                        or ptype == "finite-fault"
                    ):
                        fontsize = 9
                    top = 1
                    other_count += 1
                    vertical_dist = self.arrow_middle - self.arrow_width / 2
                    plt.vlines(elapsed, ytext, vertical_dist, colors="black")

                # plots text box for product
                plt.text(
                    elapsed,
                    ytext,
                    pstring,
                    rotation=0,
                    rotation_mode="anchor",
                    fontsize=fontsize,
                    bbox=dict(edgecolor="black", facecolor=PRODUCT_COLORS[ptype]),
                    color="black",
                )

                if ptype == "moment-tensor":
                    # adds minibit for moment-tensor

                    xy = (
                        elapsed + self.arrow_length * 0.06,
                        ytext + 0.5 * self.arrow_width,
                    )

                    if self.timeline_format == "png":
                        radius = 75
                    else:
                        radius = 20

                    bball = beach(
                        beachball_stats,
                        xy=xy,
                        size=radius,
                        width=radius,
                        axes=self.ax,
                        facecolor="#61BFFA",
                        linewidth=1,
                    )

                    self.ax.add_collection(bball)

                elif ptype == "losspager":
                    # adds minibit for PAGER
                    pager_colors = {
                        "red": "#FF0000",
                        "orange": "#FF9900",
                        "yellow": "#FFFF00",
                        "green": "#00B04F",
                        "pending": "white",
                    }

                    color = pager_colors[product_summary.lower()]

                    self.make_text_minibit(
                        color, product_summary.upper(), elapsed, ytext
                    )

                elif ptype == "finite-fault":
                    # adds minibit for finite-fault

                    length, width = self.finite_fault_text()

                    text = f"L: {length} \nW: {width}"

                    self.make_text_minibit("#E3E8FC", text, elapsed, ytext, 8.5)

                elif ptype == "shakemap":
                    # adds the minibit for the shakemap
                    roman_numerals = {
                        0: "0",
                        1: "I",
                        2: "II",
                        3: "III",
                        4: "IV",
                        5: "V",
                        6: "VI",
                        7: "VII",
                        8: "VIII",
                        9: "IX",
                        10: "X",
                    }
                    palette = ColorPalette.fromPreset("mmi")
                    color = palette.getDataColor(
                        float(product_summary), color_format="hex"
                    )
                    text_sm = roman_numerals[int(round(float(product_summary)))]
                    self.make_text_minibit(color, text_sm, elapsed, ytext)

                elif ptype == "origin":
                    # adds the minibit for the origin
                    self.make_text_minibit("#8AFF8A", product_summary, elapsed, ytext)

                elif ptype == "ground-failure":

                    # landslide and liquefaction img options
                    landslide_imgs = {
                        "red": "gf-landslide-red.png",
                        "green": "gf-landslide-green.png",
                        "yellow": "gf-landslide-yellow.png",
                        "orange": "gf-landslide-orange.png",
                    }
                    liquefaction_imgs = {
                        "red": "gf-liquefaction-red.png",
                        "green": "gf-liquefaction-green.png",
                        "yellow": "gf-liquefaction-yellow.png",
                        "orange": "gf-liquefaction-orange.png",
                    }

                    if landslide != "pending":
                        # plots the correct image
                        landslide_path = (
                            pathlib.Path(__file__).parent
                            / "data"
                            / str(landslide_imgs[landslide])
                        )
                        landslide_img = plt.imread(landslide_path)
                        imagebox = OffsetImage(landslide_img, zoom=0.05)
                        ab = AnnotationBbox(
                            imagebox,
                            (
                                elapsed + 0.02 * self.arrow_length,
                                ytext + 0.45 * self.arrow_width,
                            ),
                            frameon=False,
                        )
                        self.ax.add_artist(ab)

                    if liquefaction != "pending":
                        liquefaction_path = (
                            pathlib.Path(__file__).parent
                            / "data"
                            / str(liquefaction_imgs[liquefaction])
                        )
                        liquefaction_img = plt.imread(liquefaction_path)
                        imagebox = OffsetImage(liquefaction_img, zoom=0.05)
                        ab = AnnotationBbox(
                            imagebox,
                            (
                                elapsed + 0.055 * self.arrow_length,
                                ytext + 0.45 * self.arrow_width,
                            ),
                            frameon=False,
                        )
                        self.ax.add_artist(ab)

                    if liquefaction == "pending" and landslide == "pending":
                        self.make_text_minibit("white", "PENDING", elapsed, ytext)

                elif ptype == "oaf":
                    # if ptype is oaf, the first oaf is being added and should
                    #  be plotted, adds minibit
                    self.make_text_minibit("#CACAB0", product_summary, elapsed, ytext)

            elif ptype == "dyfi":
                # adds data point to x and y values if product is dyfi
                ypos = self.arrow_middle + self.arrow_width * 20 * (
                    int(row["Description"].split("|")[1].split("# ")[1])
                    / int(self.nresp)
                )

                if int(row["Description"].split("|")[1].split("# ")[1]) != 0 and (
                    len(dyfi_y) == 0 or (ypos) >= dyfi_y[-1]
                ):
                    dyfi_x.append(elapsed)
                    dyfi_y.append(ypos)

                dyfi = True

            elif ptype == "oaf":
                # gets percentages and occurrences if product is oaf
                percentages, occurrences = self.oaf_data()

                oaf = True

        if dyfi:
            # plots the DYFI responses in the background
            color = PRODUCT_COLORS["dyfi"]
            self.ax.scatter(dyfi_x, dyfi_y, color=color, zorder=-1, alpha=0.3)
            self.ax.plot(dyfi_x, dyfi_y, color=color, zorder=-1, linewidth=3, alpha=0.3)
        else:
            print("No DYFI responses to plot.")

        if oaf and percentages != -1:
            # creates a table of the likelihood of aftershocks or the number
            # of aftershocks that have occurred
            magnitude = ["Magnitude", "3+", "4+", "5+", "6+", "7+"]
            table_text = [magnitude, percentages, occurrences]

            bbox = [0.85, -0.15, 0.15, 0.1]
            colWidths = [0.05, 0.02, 0.02, 0.02, 0.02, 0.02]
            color = PRODUCT_COLORS["oaf"]
            cellColours = [color, color, color, color, color, color]
            self.ax.table(
                cellText=table_text,
                loc="lower right",
                fontsize=8,
                bbox=bbox,
                colWidths=colWidths,
                cellLoc="center",
                cellColours=[cellColours, cellColours, cellColours],
            )

            self.ax.text(
                0.85,
                -0.045,
                "Aftershock Forecast",
                fontsize=8,
                transform=self.ax.transAxes,
            )

        else:
            print("No available OAF data.")

    def plot_elapsed_time(self, elapsed_time, start, end):
        """Plots the text boxes describing the skipped time frames

        Args:
            elapsed_time (float): the position to plot the text boxes
            start (int): when the time skip starts
            end (int): when the time skip ends
        """
        plt.vlines(
            self.arrow_length * (elapsed_time - 0.005),
            self.arrow_middle - 1.5 * self.arrow_width,
            self.arrow_middle + self.arrow_width / 2,
            colors="red",
        )

        plt.text(
            (elapsed_time - 0.005) * self.arrow_length,
            self.arrow_middle - 1.5 * self.arrow_width,
            f"{start}-{end}h",
            rotation=0,
            rotation_mode="anchor",
            fontsize=7,
            bbox=dict(facecolor="white", edgecolor="red"),
        )

    def finite_fault_text(self):
        """Calculates the length and width of the fault.

        Returns:
            length (float): The calculated length of the fault.
            width (float): The calculated width of the fault.
            boolean: Whether the finite-fault should be plotted on the timeline.
        """

        # creating an origin dictionary to turn into an Origin object
        origin = {}

        origin["id"] = self.event_details.id
        origin["time"] = self.event_details.time
        origin["locstring"] = self.event_details.location
        origin["lat"] = self.event_details.latitude
        origin["lon"] = self.event_details.longitude
        origin["depth"] = self.event_details.depth
        origin["mag"] = self.event_details.magnitude
        origin["alert"] = self.event_details.alert
        origin["netid"] = self.event_details["net"]
        origin["network"] = ""

        origin = Origin(origin)

        # collecting and reading the finite-fault json file
        ffault = self.event_details.getProducts("finite-fault", version="all")[self.finite_fault_count]

        self.finite_fault_count += 1

        if "shakemap_polygon.txt" not in ffault.contents:
            return "N/A", "N/A"

        contents, _ = ffault.getContentBytes("shakemap_polygon.txt")
        fobj = StringIO(contents.decode("utf8"))
        all_lines = fobj.readlines()

        lines = [line for line in all_lines if not line.startswith("#")]

        if not len(lines):
            return "N/A", "N/A"

        data = []
        for line in lines:
            row = line.strip().split()
            data.append(row)

        # creating a QuadRupture object to calculate length and width
        quad = QuadRupture.fromVertices(
            [data[0][0]],
            [data[0][1]],
            [data[0][2]],
            [data[1][0]],
            [data[1][1]],
            [data[1][2]],
            [data[2][0]],
            [data[2][1]],
            [data[2][2]],
            [data[3][0]],
            [data[3][1]],
            [data[3][2]],
            origin,
        )

        length = round(quad.getLength(), 2)
        width = round(quad.getWidth(), 2)

        return length, width

    def oaf_data(self):
        """Collects data from the aftershock forecast, specifically the
        probability of aftershocks happening in the week after the initial
        event, and the the number of aftershocks that have occurred thus far.

        Returns:
            percentages (list): A list of likelihoods of aftershocks.
            occurrences (list): A list of the afteshocks that have occurred.
        """

        magnitudes = ["3.0", "4.0", "5.0", "6.0", "7.0"]

        # collect and load the oaf json file
        oaf = self.event_details.getProducts("oaf")[0]

        if "forecast.json" in oaf.contents:
            data, _ = oaf.getContentBytes("forecast.json")
            forecast_key = "forecast"
        elif "forecast_data.json" in oaf.contents:
            data, _ = oaf.getContentBytes("forecast_data.json")
            forecast_key = "results"
        else:
            return -1, -1

        fobj = StringIO(data.decode("utf8"))
        jdict = json.load(fobj)

        percentages = ["% Week 1"]
        occurrences = ["Occurrences"]

        if forecast_key == "forecast":
            file = jdict[forecast_key]
            observations_key = jdict["observations"]
        elif forecast_key == "results":
            file = jdict[forecast_key]["generic_json"]["forecast"]
            observations_key = jdict[forecast_key]["generic_json"]["observations"]

        # collecting percentages and occurrences
        for forecast in file:
            if forecast["label"] == "1 Week":
                j = 0
                for i in range(0, len(forecast["bins"])):
                    while str(forecast["bins"][i]["magnitude"]) != magnitudes[
                        j
                    ] and j < len(magnitudes):
                        j += 1
                        percentages.append("N/A")
                    percentage = (
                        f"{int(float(forecast['bins'][i]['probability'])*100)}%"
                    )
                    if percentage == "0%":
                        percentage = "< 1%"
                    percentages.append(percentage)
                    j += 1

        j = 0
        for i in range(0, len(observations_key)):
            while str(observations_key[i]["magnitude"]) != magnitudes[j]:
                j += 1
                occurrences.append("N/A")
            occurrences.append(observations_key[i]["count"])
            j += 1

        return percentages, occurrences

    def plot_arrow(self):
        """Plots the timeline arrow"""

        self.figure, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
        plt.sca(self.ax)
        # draws an arrow representing the timeline
        self.arrow_middle = 0.5
        self.arrow_width = 0.01
        self.arrow_length = np.ceil(
            self.shortened_history.iloc[-1]["Elapsed (min)"] / 60
        )
        self.head_length = self.arrow_length * 0.05
        head_width = self.arrow_width * 2
        plt.arrow(
            0,
            self.arrow_middle,
            self.arrow_length,
            0,
            head_width=head_width,
            width=self.arrow_width,
            head_length=self.head_length,
            facecolor=(200 / 255, 200 / 255, 200 / 255),
        )

    def plot_times(self):
        """Plots the important/notable times of the plot"""
        # times that will show up on the timeline if their time block is given space
        notable_times = [
            (0, "Origin"),
            (10, "10 min"),
            (20, "20 min"),
            (30, "30 min"),
            (60, "1 h"),
            (120, "2 h"),
            (180, "3 h", [0, 1]),
            (240, "4 h", [0, 1, 3]),
            (420, "7 h", [0, 1, 3, 4]),
            (600, "10 h", [0, 1, 3, 4, 7]),
            (1200, "20 h", [0, 1, 3, 4, 7, 10]),
            (1440, "1 d", [0, 1, 3, 4, 7, 10, 20]),
            (5760, "4 d", [0, 1, 3, 4, 7, 10, 20]),
        ]

        i = 0
        # start and end keep track of which blocks of time are skipped
        start = -1
        end = -1

        # plots the notable times on the timeline, along with blocks describing
        # time periods skipped

        max_time = self.shortened_history.iloc[-1]["Elapsed (min)"]

        while i < len(notable_times) and notable_times[i][0] < max_time:

            plot = -1

            if notable_times[i][0] <= 60:
                # if time is less than or equal to 1 hr
                if self.DEFAULT_1HR_SPACE > 0:
                    # if the 1hr block has space on timeline
                    plot = (
                        notable_times[i][0]
                        / 60
                        * self.DEFAULT_1HR_SPACE
                        * self.arrow_length
                    )
                    # determine the position of the textbox for the time
                else:
                    # if no space is dedicated for 1hr start tracking how many time
                    # blocks are skipped
                    start = 0
                    end = 1
            elif notable_times[i][0] < 180:
                # if time is less than 3 hr
                if self.DEFAULT_2_3_SPACE > 0:
                    # if the 1-3hr block has space on timeline
                    plot = (
                        (notable_times[i][0] - 60)
                        / 120
                        * self.DEFAULT_2_3_SPACE
                        * self.arrow_length
                        + self.DEFAULT_1HR_SPACE * self.arrow_length
                    )  # determine the position of the textbox for the time

                    if start == 0:
                        # if the 1-3 hr block is on the timeline, but the one
                        # before it is not, create a skipped indication and reset
                        # the start value
                        self.plot_elapsed_time(self.elapsed_space["1hr"], start, end)

                        start = -1
                else:
                    # if no space is dedicated to the 1-3hr block
                    if start != 0:
                        # if the previous block was not skipped set the start and
                        # end with the start and end values of the 1-3hr block
                        start = 1
                        end = 3
                    else:
                        # if the previous block was skipped set only the end value
                        end = 3

                    if i == len(notable_times) - 1:
                        self.plot_elapsed_time(self.elapsed_space["1hr"], start, end)
            elif notable_times[i][0] < 240:
                if self.DEFAULT_4HR_SPACE > 0:
                    plot = (
                        notable_times[i][0] - 180
                    ) / 60 * self.DEFAULT_4HR_SPACE * self.arrow_length + (
                        self.elapsed_space["2-3hr"]
                    ) * self.arrow_length

                    if start in notable_times[i][2]:
                        self.plot_elapsed_time(self.elapsed_space["2-3hr"], start, end)

                        start = -1
                else:
                    if start not in notable_times[i][2]:
                        start = 3
                        end = 4
                    else:
                        end = 4

                    if i == len(notable_times) - 1:
                        self.plot_elapsed_time(self.elapsed_space["2-3hr"], start, end)
            elif notable_times[i][0] < 420:
                if self.DEFAULT_4_7_SPACE > 0.0:
                    plot = self.arrow_length * (self.DEFAULT_4_7_SPACE) * (
                        notable_times[i][0] - 240
                    ) / 180 + self.arrow_length * (self.elapsed_space["4hr"])

                    if start in notable_times[i][2]:
                        self.plot_elapsed_time(self.elapsed_space["4hr"], start, end)

                        start = -1
                else:
                    if start not in notable_times[i][2]:
                        start = 4
                        end = 7
                    else:
                        end = 7

                    if i == len(notable_times) - 1:
                        self.plot_elapsed_time(self.elapsed_space["4hr"], start, end)
            elif notable_times[i][0] < 600:
                if self.DEFAULT_7_10_SPACE > 0.0:
                    plot = self.arrow_length * (self.DEFAULT_7_10_SPACE) * (
                        notable_times[i][0] - 420
                    ) / 180 + self.arrow_length * (self.elapsed_space["4-7hr"])

                    if start in notable_times[i][2]:
                        self.plot_elapsed_time(self.elapsed_space["4-7hr"], start, end)

                        start = -1
                else:
                    if start not in notable_times[i][2]:
                        start = 7
                        end = 10
                    else:
                        end = 10

                    if i == len(notable_times) - 1:
                        self.plot_elapsed_time(self.elapsed_space["4-7hr"], start, end)
            elif notable_times[i][0] < 1200:
                if self.DEFAULT_10_20_SPACE > 0.0:
                    plot = self.arrow_length * (self.DEFAULT_10_20_SPACE) * (
                        notable_times[i][0] - 600
                    ) / 600 + self.arrow_length * (self.elapsed_space["7-10hr"])

                    if start in notable_times[i][2]:
                        self.plot_elapsed_time(self.elapsed_space["7-10hr"], start, end)

                        start = -1
                else:
                    if start not in notable_times[i][2]:
                        start = 10
                        end = 20
                    else:
                        end = 20

                    if i == len(notable_times) - 1:
                        self.plot_elapsed_time(self.elapsed_space["7-10hr"], start, end)
            elif notable_times[i][0] < 1440:
                if self.DEFAULT_20_24_SPACE > 0.0:
                    plot = self.arrow_length * (self.DEFAULT_20_24_SPACE) * (
                        notable_times[i][0] - 1200
                    ) / 240 + self.arrow_length * (self.elapsed_space["10-20hr"])

                    if start in notable_times[i][2]:
                        self.plot_elapsed_time(
                            self.elapsed_space["10-20hr"], start, end
                        )

                        start = -1
                else:
                    if start not in notable_times[i][2]:
                        start = 20
                        end = 24
                    else:
                        end = 24

                    if i == len(notable_times) - 1:
                        self.plot_elapsed_time(
                            self.elapsed_space["10-20hr"], start, end
                        )
            elif notable_times[i][0] >= 1440:
                if self.DEFAULT_24_SPACE > 0.0:
                    plot = self.arrow_length * (self.DEFAULT_24_SPACE) * np.log(
                        (notable_times[i][0] - 1440) / 60 / self.arrow_length + 1
                    ) + self.arrow_length * (self.elapsed_space["20-24hr"])

                    if i == len(notable_times) - 1 or start in notable_times[i][2]:
                        self.plot_elapsed_time(
                            self.elapsed_space["20-24hr"], start, end
                        )

            if plot != -1:
                self.plot_time_box(notable_times[i][1], plot)
            i += 1

        self.plot_time_box(notable_times[i][1], self.arrow_length)

    def plot_dyfi(self):
        """Creates the dyfi axis"""
        plt.vlines(
            self.arrow_length + self.head_length,
            self.arrow_middle,
            self.arrow_middle + 20 * self.arrow_width,
            colors=PRODUCT_COLORS["dyfi"],
        )

        self.nresp = (
            self.dyfi_frame.tail(1)["Description"]
            .values[0]
            .split("|")[1]
            .split("# ")[1]
        )

        if int(self.nresp) < 10:
            self.nresp = 10

        order = max(math.floor(np.log10(int(self.nresp))), 1)
        max_dyfi = math.ceil(int(self.nresp) / (10**order)) * 10**order

        for i in range(1, 11):
            tick_dyfi = int(max_dyfi * 0.1 * i)
            plt.text(
                self.arrow_length + self.head_length,
                self.arrow_middle + self.arrow_width * 20 * 0.1 * i,
                tick_dyfi,
                fontsize=7,
                bbox=dict(facecolor="white", edgecolor=PRODUCT_COLORS["dyfi"]),
                color=PRODUCT_COLORS["dyfi"],
            )

        plt.text(
            self.arrow_length + self.head_length,
            self.arrow_middle + self.arrow_width * 20 * 1.1,
            "DYFI \n Responses",
            fontsize=7,
            bbox=dict(facecolor="white", edgecolor=PRODUCT_COLORS["dyfi"]),
            color=PRODUCT_COLORS["dyfi"],
        )

    def plot_legend(self):
        """Creates the legend"""

        products = [
            "Origin",
            "Shakemap",
            "PAGER",
            "Finite-fault",
            "Ground-failure",
            "Moment-tensor",
            "Operational \n Aftershock \n Forecast",
        ]

        cellColours = []
        for product in products:
            if product == "PAGER":
                product = "losspager"
            elif product == "Operational \n Aftershock \n Forecast":
                product = "oaf"
            cellColours.append([PRODUCT_COLORS[product.lower()]])

        bbox = [0.005, 0.95, 0.07, 0.2]

        cellText = [[product] for product in products]

        table = self.ax.table(
            cellText=cellText,
            loc="upper left",
            fontsize=8,
            cellLoc="center",
            colWidths=[0.07],
            cellColours=cellColours,
            bbox=bbox,
        )

        cellDict = table.get_celld()
        cellDict[(6, 0)].set_height(0.05)

    def plot_time_box(self, time, location):
        plt.text(
            location,
            self.arrow_middle,
            time,
            rotation=0,
            rotation_mode="anchor",
            fontsize=7,
            bbox=dict(facecolor="white"),
        )

        plt.vlines(
            location,
            self.arrow_middle - self.arrow_width,
            self.arrow_middle + self.arrow_width,
            colors="black",
        )

    def make_text_minibit(self, color, minibit, x, y, fontsize=9):
        plt.text(
            x + self.arrow_length * 0.005,
            y - 0.1 * self.arrow_width,
            minibit,
            rotation=0,
            rotation_mode="anchor",
            fontsize=fontsize,
            bbox=dict(facecolor=color, pad=1),
        )

    def deleted(self, color, x, pstring):
        plt.text(
            x,
            self.arrow_middle - 2.25 * self.arrow_width,
            pstring,
            rotation=0,
            rotation_mode="anchor",
            fontsize=7,
            color=color,
            bbox=dict(edgecolor=color, facecolor="white", pad=1),
        )

        plt.vlines(
            x,
            self.arrow_middle - 2.25 * self.arrow_width,
            self.arrow_middle + self.arrow_width / 2,
            colors="red",
        )
