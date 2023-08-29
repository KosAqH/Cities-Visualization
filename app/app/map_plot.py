from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly
import json

import base64
from io import BytesIO

class MapPlot():
    def __init__(self, df, requested_data) -> None:
        self.request = requested_data
        self.df = df
    
    def match_string(self,
                     phrase: str,
                     pos: str, 
                     color: str) -> pd.DataFrame:
        print(self.df.columns)
        
        if pos == "Starts":
            new_df = self.df[self.df["name"].str.startswith(phrase.capitalize())].copy()
        elif pos == "Ends":
            new_df = self.df[self.df["name"].str.endswith(phrase)].copy()
        elif pos == "Contains":
            new_df = self.df[self.df["name"].str.contains(phrase)].copy()

        new_df["color"] = color
        return new_df


    def query(self, df:pd.DataFrame = None, query: dict = {}):
        print(self.df.shape)
        if "only_indepedent" in self.request and self.request["only_indepedent"]:
            index = self.df[~self.df["higher_rank_object_name"].isna()].index
            print(index)
            self.df.drop(index, inplace=True, axis=0)
            print("only indepedent")
        if "only_official" in self.request and self.request["only_official"]:
            index = self.df[self.df["status"] != "urzędowa"].index
            print(index)
            self.df.drop(index, inplace=True, axis=0)
            print("only official")
        
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

    def prepare_label(self, phrase, pos):
        if pos == "Starts":
            return f"{phrase}-"
        elif pos == "Ends":
            return f"-{phrase}"
        else:
            return phrase

class MapPlotStatic(MapPlot):
    def plot(self):
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

        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"  

class MapPlotDynamic(MapPlot):
    def plot(self):
        labels = {
            self.request["color1"]: self.prepare_label(self.request["phrase1"], 
                                                       self.request["positioning1"]),
            self.request["color2"]: self.prepare_label(self.request["phrase2"], 
                                                       self.request["positioning2"]),                                           
        }
        labels_flip = dict((v, k) for k, v in labels.items())
        for c in labels.keys():
            self.df.loc[(self.df["color"] == c),"phrase"] = labels[c]


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
                            y=0.01,
                            xanchor="left",
                            x=0.01)
                            )
        
        
        return fig.to_html(include_plotlyjs =False, full_html=False)


def plotStatic():
    fig = plt.figure(figsize=(10, 10))
    m = Basemap(projection="lcc", resolution='i', 
                width=7e5, height=7e5, 
                lat_0=52, lon_0=19.2,
                )

    m.drawcoastlines(linewidth = 1)
    m.drawcountries(linewidth = 2)
    m.drawrivers(linewidth = 1, color="#add8e6")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def plotDynamicDefault():
    fig = px.scatter_mapbox(
                        zoom=5,
                        size_max=15,
                        center={
                            "lat": 52,
                            "lon": 19
                        })
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig.to_html(include_plotlyjs =False, full_html=False)

if __name__ == "__main__":
    pass