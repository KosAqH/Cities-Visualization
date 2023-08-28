from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly
import json

import base64
from io import BytesIO

def query(df:pd.DataFrame, query: dict):
    print(df.shape)
    if query["all_names"] == 'n':
        print("not all names")
        if query["only_indepedent"]:
            index = df[~df["higher_rank_object_name"].isna()]
            df.drop(index, inplace=True)
            print("only indepedent")
        if query["only_official"]:
            index = df[df["status"] == "urzędowa"]
            df.drop(index, inplace=True)
            print("only official")
    print(df.shape)
    
    # 1st condition
    len1 = len(query["phrase1"])
    if query["positioning1"] == "Starts":
        df1 = df[df["name"].str.startswith(query["phrase1"])].copy()
    elif query["positioning1"] == "Ends":
        df1 = df[df["name"].str.endswith(query["phrase1"])].copy()
    elif query["positioning1"] == "Contains":
        df1 = df[df["name"].str.contains(query["phrase1"])].copy()

    print(df1.shape)
    
    # 2nd condition
    len2 = len(query["phrase2"])
    if query["positioning2"] == "Starts":
        df2 = df[df["name"].str.startswith(query["phrase2"])].copy()
    elif query["positioning2"] == "Ends":
        df2 = df[df["name"].str.endswith(query["phrase2"])].copy()
    elif query["positioning2"] == "Contains":
        df2 = df[df["name"].str.contains(query["phrase2"])].copy()

    print(df2.shape)

    df = pd.concat((df1, df2)).drop_duplicates()

    return df

def plotStatic(df, config={}):
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
        df[df["name"].str[-3:] == "owo"]["dd_lon"].values.tolist(),
        df[df["name"].str[-3:] == "owo"]["dd_lat"].values.tolist()
    )

    m.scatter(x, y, color="red", label="owo", alpha=0.5)

    x, y = m(
        df[df["name"].str[-2:] == "ów"]["dd_lon"].values.tolist(),
        df[df["name"].str[-2:] == "ów"]["dd_lat"].values.tolist()
    )

    m.scatter(x, y, color="blue", label="ów", alpha=0.5)
    plt.legend(loc='lower left', fontsize='xx-large', framealpha=1)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def plotDynamic(df, config={}):
    fig = px.scatter_mapbox(df[:100], 
                        lat="dd_lat",
                        lon="dd_lon", # which column to use to set the color of markers
                        hover_name="name", # column added to hover information
                        hover_data={
                            "dd_lat": False,
                            "dd_lon": False
                        },
                        zoom=6,
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