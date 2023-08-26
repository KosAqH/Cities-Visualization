from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import base64
from io import BytesIO


def plotStatic(df):
    fig = plt.figure(figsize=(8, 8))
    m = Basemap(projection="lcc", resolution='i', 
                width=8e5, height=8e5, 
                lat_0=52, lon_0=19,
                )

    m.drawcoastlines(linewidth = 1)
    m.drawcountries(linewidth = 2)
    m.drawrivers(linewidth = 1, color="#add8e6")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"




if __name__ == "__main__":
    pass