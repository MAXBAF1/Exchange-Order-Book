import numpy as np
import pandas as pd
from pandas import DataFrame as df
from binance.client import Client
import keys
import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import time

# Load data
client = Client(api_key = keys.Pkey , api_secret = keys.Skey)


def convertor(s):
	try :
		int(s.rstrip('0').rstrip('.'))
		return 0
	except:
		return len(str(float(s)).split('.')[-1])

def price_lot(ba, symb, limit):
    limit = limit
    candles = client.get_order_book(symbol=symb, limit=limit)

    price_list = []
    lot_list = []
    for i in range(len(candles['bids'])):
        price = float(candles[ba][i][0])
        lot = round(float(candles[ba][i][1]))

        if price in price_list and lot != 0:
            ind = price_list.index(price)
            zam = lot_list[ind] + lot
            lot_list.pop(ind)
            lot_list.insert(ind,zam)
        elif lot != 0:
            price_list.append(price)
            lot_list.append(lot)
    return [price_list,lot_list]

def reb():
    global symb
    symb = str(entr.get())
    limit = str(limitentr.get())
    bids = price_lot('bids', symb, limit)
    asks = price_lot('asks', symb, limit)

    #Цены бид и аск
    bid_price = bids[0]
    ask_price = asks[0]

    #Лоты бид и аск
    bid_lot = bids[1]
    ask_lot = asks[1]


    max_bid_lot = max(bid_lot)    #Максимальный бид лот
    max_ask_lot = max(ask_lot)  # Максимальный бид лот

    if max_bid_lot > max_ask_lot: # Максимальный лот
        max_lot = max_bid_lot
        fair = 1
    else:
        max_lot = max_ask_lot
        fair = 0

    if fair == 1: #Цена максимального лота
        indexlot = bid_lot.index(max_lot)
        price_max_lot = bid_price[indexlot]
    else:
        indexlot = ask_lot.index(max_lot)
        price_max_lot = ask_price[indexlot]


    if max_lot > int(countentr.get()):
        bgc = 'red'
    else:
        bgc = 'lime green'

    if len(str(round(max_lot))) > 3 and len(str(round(max_lot))) < 6:
        max_lot_fin = str(round( (round(max_lot) / 1000), 1)) + 'K'
    elif len(str(round(max_lot))) > 6:
        max_lot_fin = str(round( (round(max_lot) / 1000000), 1)) + 'M'
    else:
        max_lot_fin = str(round(max_lot))
    lbl.config(text = (price_max_lot, '-', max_lot_fin), font = ('arial', 15, BOLD), bg = bgc)
    frame1.config(text = symb)





window = tk.Tk()
window.geometry('1000x500')
window.title("Стакан")

###BTCUSDT
value = 'BTCUSDT'
frame1 = tk.LabelFrame(window, text = value, font = ('arial', 10, BOLD))

frame11 = tk.Frame(frame1)
lbl = tk.Label(frame11)
entr = tk.Entry(frame11, textvariable = tk.StringVar(frame11, value = value), font = ('arial', 10, BOLD), justify = 'center', highlightthickness=1, highlightbackground="gray")
lbl.pack(expand = 1, fill = 'both')
entr.pack(fill = 'both')
frame11.grid(row = 0, column = 0, padx = 10, pady = 10, ipadx = 20, ipady = 20)

frame12 = tk.Frame(frame1)
countlbl = tk.Label(frame12, text = 'Лимит:')
countentr = tk.Entry(frame12, textvariable = tk.StringVar(frame12, value = 100), highlightthickness=1, highlightbackground="gray")
countlbl.grid(row = 0, column = 0, sticky = 'w')
countentr.grid(row = 0, column = 1, sticky = 'w')
frame12.grid(row = 1, column = 0, padx = 10, pady = (0, 10))

frame13 = tk.Frame(frame1)
limitlbl = tk.Label(frame13, text = 'Кол-во данных:')
limitentr = tk.Entry(frame13, textvariable = tk.StringVar(frame13, value = 1000), width = 10, highlightthickness=1, highlightbackground="gray")
limitlbl.grid(row = 0, column = 0, sticky = 'w')
limitentr.grid(row = 0, column = 1, sticky = 'w')
frame13.grid(row = 2, column = 0, padx = 10, pady = (0, 10))

frame1.grid(row=0, column=0, padx = 10, pady = 10)




btn = tk.Button(window, text='Обновить', font=10, command=reb)
btn.place(x = 500, y = 100)


reb()
window.mainloop()







