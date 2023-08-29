from . import app
from flask import render_template, request
import pandas as pd

from . import map_plot as mp
from .forms import MapInput

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        df = pd.read_csv("data\\prepared_data.csv")

        obj_static = mp.MapPlotStatic(df, dict(request.form))
        obj_static.query()
        ms = obj_static.plot()

        obj_dynamic = mp.MapPlotDynamic(df, dict(request.form))
        obj_dynamic.query()
        md = obj_dynamic.plot()
    else:
        ms = mp.plotStatic()
        md = mp.plotDynamicDefault()

    input_form = MapInput()
    return render_template('index.html', map_static=ms, map_dynamic=md, form=input_form)
