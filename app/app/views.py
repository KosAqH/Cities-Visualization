from . import app
from flask import render_template
import pandas as pd

from . import map_plot as mp

@app.route("/")
def index():

    df = pd.read_csv("data\\prepared_data.csv")
    m = mp.plotStatic(df)
    
    return render_template('index.html', map_static=m)
