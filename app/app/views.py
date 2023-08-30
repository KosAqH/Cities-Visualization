from . import app
from flask import render_template, request, jsonify
import pandas as pd
import re

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

@app.route("/static_plot", methods=["POST"])
def staticPlot():
    if request.method == 'POST':
        df = pd.read_csv("data\\prepared_data.csv")
        obj_static = mp.MapPlotStatic(df, dict(request.form))
        obj_static.query()
        ms = obj_static.plot()
        # ms = "teścik"

    return jsonify(ms)

@app.route("/dynamic_plot", methods=["POST"])
def dynamicPlot():
    if request.method == 'POST':
        df = pd.read_csv("data\\prepared_data.csv")
        obj_dynamic = mp.MapPlotDynamic(df, dict(request.form))
        obj_dynamic.query()
        md = obj_dynamic.plot()

    l = re.findall(r"<script(.*?)>(.*?)</script>", md)

    response = {
        "div" : f"<div {re.findall(r'<div (.+?)></div>', md)[0]}></div>",
        "script": l[0][1]
    }
    print(response)
    return jsonify(response)