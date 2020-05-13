from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
import io
import yfinance as yf
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import base64

plt.switch_backend('Agg')

def get_data(tickers):
    hist = []
    last = []
    for i, ticker in enumerate(tickers):
        hist_tmp = yf.Ticker(ticker).history(period='max')
        if len(hist_tmp)>0:
            last_tmp = float(hist_tmp['Close'].iloc[-1])
        else:
            last_tmp = 0
        hist.append(hist_tmp)
        last.append(last_tmp)
    return last, hist

def fin_plot(hists, ticker, coords, legend_vals):

    beaut_space = 20
    fig = plt.figure(figsize=(16, 8), dpi=80)
    axis = fig.add_subplot(1, 1, 1)

    for el in hists:
        axis.plot(el['line']['period'], el['line']['Close'], color = el['color'], linewidth = el['width'])
        #axis.scatter(el['line']['period'], el['line']['Close'], color= el['color'], marker='.',  linewidth= el['width'])
    axis.set(title=ticker, ylabel='Price', xlabel='Timeline')

    for xc in coords.keys():
        plt.axvline(xc, color = coords[xc])

    patchList = []
    for val in legend_vals:
        len_key = len(val['key'])
        lbl = val['key']+' '*(beaut_space-len_key)+str(val['label'])
        data_key = mpl_patches.Patch(linewidth = 0, color=val['color'], label=lbl)
        patchList.append(data_key)
    leg = plt.legend(handles=patchList, handlelength=0, loc = 2)
    for text, color in zip(leg.get_texts(),legend_vals):
        text.set_color(color['color'])

    plt.grid(b = True,  which = 'major', linestyle = '--')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return f'<img src="data:image/png;base64,{plot_url}">'

def xcoords(direction, enter_dt, exit_dt):
    today = datetime.today().strftime('%Y-%m-%d')
    if(enter_dt=="" and len(exit_dt)==10):
        enter_dt = str(today)
    if(exit_dt=="" and len(enter_dt)==10):
        exit_dt = str(today)
    if(exit_dt=="" and enter_dt=="" and direction!=""):
        enter_dt = str(today)
        exit_dt = str(today)
    if direction=='buy':
        coords = {
        datetime.strptime(enter_dt, '%Y-%m-%d'):'green',
        datetime.strptime(exit_dt, '%Y-%m-%d'):'red',
        }
    elif direction=='sell':
        coords = {
        datetime.strptime(enter_dt, '%Y-%m-%d'):'red',
        datetime.strptime(exit_dt, '%Y-%m-%d'):'green',
        }
    else:
        coords = {}
    return coords


def xcoords_i(direction, enter_dt, exit_dt):
    today = datetime.today().strftime('%Y-%m-%d')
    if(enter_dt=="" and len(exit_dt)==10):
        enter_dt = str(today)
    if(exit_dt=="" and len(enter_dt)==10):
        exit_dt = str(today)
    if(exit_dt=="" and enter_dt=="" and direction!=""):
        enter_dt = str(today)
        exit_dt = str(today)
    if direction=='buy':
        coords = {
        'enter':{'point':enter_dt, 'color':'green', 'label':'BUY'},
        'exit':{'point':exit_dt, 'color':'red', 'label':'SELL'}
        }
    elif direction=='sell':
        coords = {
        'enter':{'point':enter_dt, 'color':'red', 'label':'SELL'},
        'exit':{'point':exit_dt, 'color':'green', 'label':'BUY'}
        }
    else:
        coords = {}
    return coords

def legends(last, direction, enter_dt, exit_dt, y5, y10, y15, y20):
    today = datetime.today().strftime('%Y-%m-%d')
    if(enter_dt=="" and len(exit_dt)==10):
        enter_dt = str(today)
    if(exit_dt=="" and len(enter_dt)==10):
        exit_dt = str(today)
    if(exit_dt=="" and enter_dt=="" and direction!=""):
        enter_dt = str(today)
        exit_dt = str(today)
    if direction=='buy':
        buy = enter_dt
        sell = exit_dt
    elif direction=='sell':
        buy = exit_dt
        sell = enter_dt
    else:
        buy = ''
        sell = ''
    fin_lst = [{'key':'BUY', 'label':buy, 'color':'green'},
               {'key':'SELL', 'label':sell, 'color':'red'},
               {'key':'LAST', 'label':last, 'color':'blue'}]
    if(y5):
        fin_lst.append({'key':'5 Years', 'label':'', 'color':'red'})
    if(y10):
        fin_lst.append({'key':'10 Years', 'label':'', 'color':'green'})
    if(y15):
        fin_lst.append({'key':'15 Years', 'label':'', 'color':'blue'})
    if(y20):
        fin_lst.append({'key':'20 Years', 'label':'', 'color':'yellow'})
    return fin_lst


def shift_years(hist, years = 5, period = 12):
    hist['period'] = hist.index
    left = (hist['period']<datetime.now() - relativedelta(months = years*12 - int(max(period/4, 3))))
    right = (hist['period']>datetime.now() - relativedelta(months=(12*years+period)))
    y_ind = left & right
    hist_tmp = hist[y_ind]
    hist_tmp['period'] = pd.to_datetime(hist_tmp['period']).dt.date+relativedelta(years = years)
    return hist_tmp[['period','Close']]

def shift_years_i(hist, years = 5, period = 12):
    hist['period'] = hist.index
    left = (hist['period']<datetime.now() - relativedelta(months = years*12 - int(max(period/4, 3))))
    right = (hist['period']>datetime.now() - relativedelta(months=(12*years+period)))
    y_ind = left & right
    hist_tmp = hist[y_ind]
    hist_tmp['period'] = pd.to_datetime(hist_tmp['period']).dt.date+relativedelta(years = years)
    hist_tmp['period'] = pd.to_datetime(hist_tmp['period']).dt.strftime('%Y-%m-%d')
    return hist_tmp[['period','Open','High','Low','Close', 'Volume']]

def f_plot_dict(hist, period, y5, y10, y15, y20):
    plot_dict = [{'color':'black', 'width':1,'line':shift_years(hist,0,period)}]
    if(y5==1):
        plot_dict.append({'color':'red', 'width':1,'line':shift_years(hist,5,period)})
    if(y10==1):
        plot_dict.append({'color':'green', 'width':1,'line':shift_years(hist,10,period)})
    if(y15==1):
        plot_dict.append({'color':'blue', 'width':1,'line':shift_years(hist,15,period)})
    if(y20==1):
        plot_dict.append({'color':'yellow', 'width':1,'line':shift_years(hist,20,period)})
    return plot_dict


def f_plot_dict_i(hist, period, ticker, y5, y10, y15, y20):
#    hist['period'] = pd.to_datetime(hist['period']).dt.strftime('%Y-%m-%d').astype(str)
    plot_dict = [{'color':'black', 'width':1,'line':shift_years_i(hist,0,period).values.tolist(), 'name':ticker}]
    if(y5==1):
        plot_dict.append({'color':'red', 'width':1,'line':shift_years_i(hist,5,period).values.tolist(), 'name':'5 Years'})
    if(y10==1):
        plot_dict.append({'color':'green', 'width':1,'line':shift_years_i(hist,10,period).values.tolist(), 'name':'10 Years'})
    if(y15==1):
        plot_dict.append({'color':'blue', 'width':1,'line':shift_years_i(hist,15,period).values.tolist(), 'name':'15 Years'})
    if(y20==1):
        plot_dict.append({'color':'yellow', 'width':1,'line':shift_years_i(hist,20,period).values.tolist(), 'name':'20 Years'})
    return plot_dict
