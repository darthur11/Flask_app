
from flask import render_template, Response, request, Flask
from app import app
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
import io
import random
import yfinance as yf
import datetime as dt
import pandas as pd
import base64
import json

plt.switch_backend('Agg')

def get_data(ticker, period):
    return yf.Ticker(ticker).history(period=period)

def fin_plot(hist, ticker):

    beaut_space = 20
    fig = plt.figure(figsize=(16, 8), dpi=80)
    axis = fig.add_subplot(1, 1, 1)

    hist['period'] = hist.index

    axis.plot(hist['period'], hist['Close'], color = 'black', linewidth = 1)
    axis.scatter(hist.index, hist['Close'], color='black',marker='.',  linewidth= 1)
#    axis.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    axis.set(title=ticker, ylabel='Price', xlabel='Timeline')

    xcoords = [dt.datetime(2019, 9, 21), dt.datetime(2019, 10, 31), dt.datetime(2020, 3, 12)]
    for xc in xcoords:
        plt.axvline(xc, color = 'r')

    legend_dict = { 'BUY' : 'green', 'SELL' : 'red', 'POINT VALUE' : 'blue' }
    legend_vals = ['2019-04-03', '2020-08-01', '1000']
    patchList = []
    for key, val in zip(legend_dict,legend_vals):
        len_key = len(key)
        lbl = key+' '*(beaut_space-len_key)+str(val)
        data_key = mpl_patches.Patch(linewidth = 0, color=legend_dict[key], label=lbl)
        patchList.append(data_key)
    leg = plt.legend(handles=patchList, handlelength=0)
    for text, color in zip(leg.get_texts(),legend_dict.values()):
        text.set_color(color)

    plt.grid(b = True,  which = 'major', linestyle = '--')

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")
#    FigureCanvasAgg(fig).print_png(output)
#    return Response(output.getvalue(), mimetype="image/png")


@app.route("/")
def index():
    return render_template('index.html', title='Home')


@app.route("/fin_data")
def plot_svg2(ticker="MSFT", period="1y"):
    return render_template('base.html', title='Home')
