from requests import get
import json
import gspread
from time import sleep
from time import time
from tkinter import *
from tkinter import ttk
from multiprocessing import Process

def parser(url):
    print('parser')
    data = get(url)
    obj = json.loads(data.text)
    massiv = {}
    needed = obj['data']['ticker']
    for ticker in needed:
        massiv.setdefault(ticker, needed[ticker]['last'])
    return massiv


def write_to_sheet(massiv, table):
    print('sheets')
    # clear = []
    # for _ in range(1000):
    #         clear.append(['', '', '', '', ''])
    # table.update(f'A1:E1001', clear)
    try:
        usdc = [['USDC', 'Цена']]
        usdt = [['USDT', 'Цена']]
        for name in massiv:
            if name.find('USDC') > 0:
                usdc.append([name, massiv[name]])
            if name.find('USDT') > 0:
                usdt.append([name, massiv[name]])
        btc_len = len(usdc)
        usdt_len = len(usdt)
        table.update(f'A1:B{usdt_len}', usdt)
        table.update(f'D1:E{btc_len}', usdc)
        print(round(time()))
    except Exception as ex:
        pass


def work():
    data = parser('https://api.coinex.com/v1/market/ticker/all')
    write_to_sheet(data, sh)


def make_button():
    root = Tk()
    root.title("button")
    root.geometry("100x70")
    btn = ttk.Button(text="Update", command=work)
    btn.pack()
    root.mainloop()


def auto():
    work()
    for _ in range(59):
        sleep(1)
    auto()


def handle():
    make_button()
    handle()


def main():
    spisok = []
    spisok.append(Process(target=auto))
    spisok.append(Process(target=handle))
    for i in spisok:
        i.start()


if __name__ == '__main__':
    with open('table_id.txt', 'r') as f:
        table_id = f.readline()
    gs = gspread.service_account(filename='api_keys.json')
    sh = gs.open_by_key(table_id).sheet1
    main()
