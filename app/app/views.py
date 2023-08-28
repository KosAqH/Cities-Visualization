from . import app
from flask import render_template
import pandas as pd

from . import map_plot as mp
from .forms import MapInput

@app.route("/")
def index():

    input_form = MapInput()

    df = pd.read_csv("data\\prepared_data.csv")
    m = mp.plotStatic(df)
    md = mp.plotDynamic(df)
    # print(md)

    return render_template('index.html', map_static=m, map_dynamic=md, form=input_form)
