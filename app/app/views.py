from . import app
from flask import render_template, request
import pandas as pd

from . import map_plot as mp
from .forms import MapInput

@app.route("/", methods=["GET", "POST"])
def index():
    df = pd.read_csv("data\\prepared_data.csv")
    graph = None
    if request.method == 'POST':
        print(request.form)
        # print(mp.query(df, dict(request.form)).sort_values(by="name"))
        obj_static = mp.MapPlotStatic(df, dict(request.form))
        obj_static.query()
        graph = obj_static.plotStatic()

    input_form = MapInput()

    df = pd.read_csv("data\\prepared_data.csv")
    # m = mp.plotStatic(df)
    
    md = mp.plotDynamic(df)
    # print(md)

    return render_template('index.html', map_static=graph, map_dynamic=md, form=input_form)
