from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import plotly.express as px
import plotly
import json

import base64
from io import BytesIO


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