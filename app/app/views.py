from . import app
from flask import render_template, request, jsonify
import pandas as pd

from . import map_plot as mp
from .forms import MapInput

@app.route("/", methods=["GET", "POST"])
def index():
    """
    View rendering main page.
    """
    input_form = MapInput()
    return render_template('index.html', form=input_form)

@app.route("/static_plot", methods=["POST"])
def staticPlot():
    """
    View returning map as a jsonifed, base64 encoded, static image
    """
    if request.method == 'POST':
        df = pd.read_csv("data\\prepared_data.csv")
        obj_static = mp.MapPlotStatic(df, dict(request.form))
        obj_static.query()
        ms = obj_static.plot()

    return jsonify(ms)

@app.route("/dynamic_plot", methods=["POST"])
def dynamicPlot():
    """
    View returning map as a jsonifed script that renders interactive map on the website.
    """
    if request.method == 'POST':
        df = pd.read_csv("data\\prepared_data.csv")
        obj_dynamic = mp.MapPlotDynamic(df, dict(request.form))
        obj_dynamic.query()
        md = obj_dynamic.plot()
        response = obj_dynamic.split_plot(md)

    return jsonify(response)