from flask import render_template, Response, request, Flask
from app import app
from functions import *
import sys

@app.route("/")
def index():
    return render_template('index.html', title='Home')


@app.route("/fin_data", methods=['GET', 'POST'])
def plot_svg2(ticker="MSFT", period="1y"):
    ticker = str(request.form.get("ticker", ""))
    period = int(request.form.get("period", 0))
    enter_dt = str(request.form.get("enter_dt", ""))
    exit_dt = str(request.form.get("exit_dt", ""))
    direction = str(request.form.get("direction", ""))
    jsss = str(request.form.get("jsss", ""))
    y5 = int(request.form.get("y5", 0))
    y10 = int(request.form.get("y10", 0))
    y15 = int(request.form.get("y15", 0))
    y20 = int(request.form.get("y20", 0))
    interactive = int(request.form.get("interactive", 0))
    last, hist = get_data(ticker)
    coords = xcoords(direction, enter_dt, exit_dt)
    legend_vals = legends(last, direction, enter_dt, exit_dt, y5, y10, y15, y20)
    plot_dict = f_plot_dict(hist, period, y5, y10, y15, y20)
    img = fin_plot(hists = plot_dict, ticker = ticker, coords = coords, legend_vals = legend_vals)
    hst = f_plot_dict_i(hist, period, ticker, y5, y10, y15, y20)
    coords_i = xcoords_i(direction, enter_dt, exit_dt)
    print(jsss, file = sys.stderr)
    if(interactive==0):
        return render_template('index.html', title='Home', img = img)
    elif(interactive==1):
        return render_template('interactive.html', title='Home', dataset = hst, coords = xcoords_i(direction, enter_dt, exit_dt))
