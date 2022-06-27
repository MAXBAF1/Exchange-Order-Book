import numpy as np
import pandas as pd
from pandas import DataFrame as df
from binance.client import Client
import keys
from tkinter import *

# Load data
client = Client(api_key = keys.Pkey , api_secret = keys.Skey)


def txt(text):
    g = []
    for i in range(len(text)):
        g.append(str(round(text[i], 6)))
    return '0\n'.join(g)

def lottxt(lottext):
    g = []
    for i in range(len(lottext)):
        g.append(str(round(lottext[i], 6)))
    return '\n'.join(g)


def func():
    c = []
    b = []
    limit = 1000
    candles = client.get_order_book(symbol='BTCUSDT', limit = limit)
    candles_data_frame = df(candles)
    #print(candles_data_frame['bids'])

    for i in range(limit):
        price = int((float(candles_data_frame['bids'][i][0])) / 10)
        lot = round(float(candles_data_frame['bids'][i][1]))

        if price in c:
            ind = c.index(price)
            zam = b[ind] + lot
            b.pop(ind)
            b.insert(ind,zam)

        else:
            c.append(price)
            b.append(lot)
    s = pd.Series(b, index = c)

    window = Tk()
    window.geometry('250x800')
    window.title("Стакан")
    text = txt(list(s.index))

    print(text)
    text = (text)
    lbl = Label(window, text=text, bg = 'green yellow')
    lbl.grid(column=0, row=0)

    lottext = lottxt(list(s.values))
    #print(lottxt(lottext))
    lbl1 = Label(window, text=lottext, bg = 'lawn green')
    lbl1.grid(column=1, row=0)

    print(s)



def func2():
    c = []
    b = []
    limit = 1000
    candles = client.get_order_book(symbol='BTCUSDT', limit = limit)
    candles_data_frame = df(candles)
    #print(candles_data_frame['bids'])

    for i in range(limit):
        price = int((float(candles_data_frame['asks'][i][0])) / 10)
        lot = round(float(candles_data_frame['asks'][i][1]))

        if price in c:
            ind = c.index(price)
            zam = b[ind] + lot
            b.pop(ind)
            b.insert(ind,zam)

        else:
            c.append(price)
            b.append(lot)
    s = pd.Series(b, index = c)

    window = Tk()
    window.geometry('250x800')
    window.title("Стакан")
    text = txt(list(s.index))

    print(text)
    text = (text)
    lbl = Label(window, text=text, bg = 'yellow')
    lbl.grid(column=0, row=0)

    lottext = lottxt(list(s.values))
    #print(lottxt(lottext))
    lbl1 = Label(window, text=lottext, bg = 'red')
    lbl1.grid(column=1, row=0)

    print(s)

    window.mainloop()

func()
func2()
