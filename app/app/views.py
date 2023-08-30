from . import app
from flask import render_template, request, jsonify
import pandas as pd
import re

from . import map_plot as mp
from .forms import MapInput

@app.route("/", methods=["GET", "POST"])
def index():
    input_form = MapInput()
    return render_template('index.html', form=input_form)

@app.route("/static_plot", methods=["POST"])
def staticPlot():
    if request.method == 'POST':
        df = pd.read_csv("data\\prepared_data.csv")
        obj_static = mp.MapPlotStatic(df, dict(request.form))
        obj_static.query()
        ms = obj_static.plot()

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

    return jsonify(response)