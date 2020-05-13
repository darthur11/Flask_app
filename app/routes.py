from flask import render_template, Response, request, Flask
from flask_wtf import Form
from wtforms.validators import InputRequired
from wtforms import SelectField, SelectMultipleField, SubmitField, RadioField, BooleanField
from app import app
from functions import *
import sys
import pandas as pd
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import DateTimeField




@app.route("/")
def index():
    return render_template('index.html', title='Home')

app.config.update(dict(
    SECRET_KEY = 'your_secret_key',
    CSRF_ENABLED = True,
))

symbols = pd.read_csv('/Users/artur.dossatayev/Documents/Algo_flask/inputs/symbols.csv')
symbols['CODE']=symbols['SYMBOL']+'=F'#symbols['EXCHANGE']+'_'+symbols['SYMBOL']
symbols = list(symbols[['CODE','NAME']].itertuples(index=False, name=None))

class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class DemoForm(Form):
    multi_select = Select2MultipleField("Ticker:", [],
            choices=symbols,
            description="",
            render_kw={"multiple": "multiple"})
    single_select = SelectField("Period:", [],
            choices=[('3', "3 Months"), ('6', "6 Months"), ('9', "9 Months"), ('12', "1 Year"), ('24', "2 Years")],
            description="",
            render_kw={"enabled": "true"})
    startdate = DateField('Start Date',default=date.today)
    enddate = DateField('End Date',default=date.today)
    radio = RadioField('direction',
            choices=[('buy','Buy'),('sell','Sell')])
    y5 = BooleanField('5 Years',
            render_kw = {'style':'outline:red 1px solid !important; margin:5px',
                        'checked': True})
    y10 = BooleanField('10 Years',
            render_kw = {'style':'outline:green 1px solid !important; margin:5px',
                        'checked': True})
    y15 = BooleanField('15 Years',
            render_kw = {'style':'outline:blue 1px solid !important; margin:5px'})
    y20 = BooleanField('20 Years',
            render_kw = {'style':'outline:yellow 1px solid !important; margin:5px'})
    interactive = BooleanField('Is interactive?')
    submit = SubmitField()



@app.route("/fin_data", methods=['GET', 'POST'])
def plot_chart():
    form = DemoForm(request.form)
    if request.method == 'POST':
        tickers = request.form.getlist('multi_select')
        period = form.single_select.data
        if period is not None:
            period = int(period)
        enter_dt = form.startdate.data
        exit_dt = form.enddate.data
        direction = form.radio.data
        y5 = form.y5.data
        y10 = form.y10.data
        y15 = form.y15.data
        y20 = form.y20.data
        interactive = form.interactive.data

        last, hist = get_data(tickers)
        coords = xcoords(direction, enter_dt, exit_dt)

        legend_vals = legends(last[0], direction, enter_dt, exit_dt, y5, y10, y15, y20)
        plot_dict = f_plot_dict(hist[0], period, y5, y10, y15, y20)

        img = fin_plot(hists = plot_dict, ticker = tickers[0], coords = coords, legend_vals = legend_vals)

        # hst = f_plot_dict_i(hist, period, ticker, y5, y10, y15, y20)
#        coords_i = xcoords_i(direction, enter_dt, exit_dt)
        return render_template('index.html', title='Home', form=form, img = img)
    else:
        interactive=0
        if(interactive==0):
            return render_template('index.html', title='Home', form=form)
        elif(interactive==1):
            return render_template('interactive.html', title='Home', dataset = hst, coords = coords_i)
