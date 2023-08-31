from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import base64
from io import BytesIO
import re

PAGE_NAME = ""

class MapPlot():
    """
    Class prepare data for plotting, considering input passed by user.

        Usage: first you have to create new object, and passed data as parameters.
            Then you should use query function to transform data. If you want to 
            plot map to visualize data, you should actually used one of derivative
            classes: MapPlotStatic or MapPlotDynamic.
 
        Attributes:
            self.df (pd.DataFrame) - main df used by class. At first it contains
                all data, after querying it contains only data that satisfy both
                conditions specified by user.
            self.request (dict) - dictionary contains conditions specified by user
            self.df1 (pd.DataFrame) - contains data that satisfy the first condition
            self.df2 (pd.DataFrame) - contains data that satisfy the second condition
    """
    def __init__(self, df: pd.DataFrame, requested_data:dict) -> None:
        """
        MapPlot class constructor. Returns nothing.

            Args:
                df (pd.DataFrame): Dataframe object containing all prepared
                    data for visualization.
                requested_data (dict): Dictionary object containing input
                    passed by user.
        """
        self.request = requested_data
        self.df = df
    
    def match_string(self,
                     phrase: str,
                     pos: str, 
                     color: str) -> pd.DataFrame:
        '''
        Returns the Dataframe containing values only for rows, where city names 
            satisfy conditions specified by user.

            Args:
                phrase (str): phrase passed by user
                pos (str): one of the following: "Starts", "Contains" or "Ends"
                color (str): one of the following: "Red", "Blue", "Green",
                    "Purple", "Black". 

            Returns:
                new_df(pd.DataFrame): The Dataframe containing only rows where 
                    city names satisfy conditions specified by user. The Dataframe
                    contains also color column, that will be used to plotting.
        '''
        phrase = phrase.lower()

        if pos == "Starts":
            new_df = self.df[self.df["name"].str.startswith(phrase)].copy()
        elif pos == "Ends":
            new_df = self.df[self.df["name"].str.endswith(phrase)].copy()
        elif pos == "Contains":
            new_df = self.df[self.df["name"].str.contains(phrase)].copy()

        new_df["color"] = color
        return new_df


    def query(self) -> None:
        '''
        Function create three Dataframes. Dataframes 'df1' and 'df2'contain 
        rows corresponding to each of the queries passed by user. Dataframe 
        'df' is a concatenation of those.
        
        No value is returned - all dataframes are saved as a class attributes.
        '''
        if "only_indepedent" in self.request and self.request["only_indepedent"]:
            index = self.df[~self.df["higher_rank_object_name"].isna()].index
            self.df.drop(index, inplace=True, axis=0)
        if "only_official" in self.request and self.request["only_official"]:
            index = self.df[self.df["status"] != "urzędowa"].index
            self.df.drop(index, inplace=True, axis=0)
        
        # 1st condition
        df1 = self.match_string( 
                        self.request["phrase1"], 
                        self.request["positioning1"], 
                        self.request["color1"])
        
        # 2nd condition
        df2 = self.match_string( 
                        self.request["phrase2"], 
                        self.request["positioning2"], 
                        self.request["color2"])

        self.df = pd.concat((df1, df2)).drop_duplicates()

        self.df1 = df1
        self.df2 = df2

    def prepare_label(self, phrase: str, pos: str) -> str:
        '''
        Returns the phrase passed by user with '-' character attached 
        at the front (if the pos parameter is equal to "Starts") or at
        the end (if the pos parameter is equal to "Ends"). For any other
        values the phrase is returned without any modifications.

            Args:
                phrase (str): phrase passed by user.
                pos (str): one of the following: "Starts", "Contains" or "Ends"

            Returns:
                phrase (str): Phrase with attached '-' character.
        '''
        if pos == "Starts":
            return f"{phrase}-"
        elif pos == "Ends":
            return f"-{phrase}"
        else:
            return phrase

class MapPlotStatic(MapPlot):
    """
    Class extends MapPlot class with creating static plots.
    """
    def plot(self) -> str:
        """
        Function creates static plot and returns it as as a base64 encoded image.

            Returns:
                plot (str): Map image encoded as base64 string.
        """
        fig = plt.figure(figsize=(10, 10))
        m = Basemap(projection="lcc", resolution='i', 
                    width=7e5, height=7e5, 
                    lat_0=52, lon_0=19.2,
                    )

        m.drawcoastlines(linewidth = 1)
        m.drawcountries(linewidth = 2)
        m.drawrivers(linewidth = 1, color="#add8e6")

        # Map (long, lat) to (x, y) for plotting
        x, y = m(
            self.df1["dd_lon"].values.tolist(),
            self.df1["dd_lat"].values.tolist()
        )

        m.scatter(x, y, 
                    color=self.request["color1"], 
                    label=self.prepare_label(self.request["phrase1"], 
                                            self.request["positioning1"]), 
                    alpha=0.5)

        x, y = m(
            self.df2["dd_lon"].values.tolist(),
            self.df2["dd_lat"].values.tolist()
        )

        m.scatter(x, y, 
                  color=self.request["color2"], 
                  label=self.prepare_label(self.request["phrase2"], 
                                           self.request["positioning2"]), 
                  alpha=0.5)
        plt.legend(loc='lower left', fontsize='xx-large', framealpha=1)
        plt.figtext(0.15, 0.08, f"Made using: {PAGE_NAME}", wrap=True, 
                    horizontalalignment='left', fontsize=10)


        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        encoded_plot = base64.b64encode(buf.getbuffer()).decode("ascii")
        plot = f"<img src='data:image/png;base64,{encoded_plot}'/>"
        return plot

class MapPlotDynamic(MapPlot):
    """
    Class extends MapPlot class with creating interactive plots.
    """
    def plot(self) -> str:
        """
        Function creates dynamic plot and returns it as as a html string.

            Returns:
                plot (str): Map image as a html string.
        """
        labels = {
            self.request["color1"]: self.prepare_label(self.request["phrase1"], 
                                                       self.request["positioning1"]),
            self.request["color2"]: self.prepare_label(self.request["phrase2"], 
                                                       self.request["positioning2"]),                                           
        }
        labels_flip = dict((v, k) for k, v in labels.items())
        for c in labels.keys():
            self.df.loc[(self.df["color"] == c),"phrase"] = labels[c]

        self.df["name"] = self.df["name"].str.capitalize()

        fig = px.scatter_mapbox(self.df, 
                            lat="dd_lat",
                            lon="dd_lon", # which column to use to set the color of markers
                            hover_name="name", # column added to hover information
                            hover_data={
                                "dd_lat": False,
                                "dd_lon": False,
                                "color": None
                            },
                            color="phrase",
                            # color_discrete_map= "identity",
                            color_discrete_map = labels_flip,
                            labels=labels,
                            zoom=5,
                            size_max=15,
                            center={
                                "lat": 52,
                                "lon": 19
                            })
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(legend=dict(
                            yanchor="bottom",
                            y=0.04,
                            xanchor="left",
                            x=0.01)
                            )
        fig.update_layout(annotations = [dict(
            x=0.01,
            y=0.01,    #Trying a negative number makes the caption disappear - I'd like the caption to be below the map
            xref='paper',
            yref='paper',
            text=f"Made using: {PAGE_NAME}",
            showarrow = False,
            bgcolor="white",
        )]
)
        
        plot = fig.to_html(include_plotlyjs = False, full_html=False)
        return plot

    def split_plot(self, plot: str) -> dict:
        """
        Function takes dynamic plot and splits it to two parts. The first is the
        actual JS script that is rendering plot on a page. The second is div, which
        is a container where plot will be put in.

            Args:
                plot (str): Map image as a html string.
            Returns:
                d (dict): Dictionary containing splitted map_image.
        """
        l = re.findall(r"<script(.*?)>(.*?)</script>", plot)
        d = {
            "div" : f"<div {re.findall(r'<div (.+?)></div>', plot)[0]}></div>",
            "script": l[0][1]
        }

        return d

if __name__ == "__main__":
    pass