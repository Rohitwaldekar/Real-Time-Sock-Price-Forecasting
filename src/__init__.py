# Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

import sys
import pathlib

import yfinance as yf

def historic_data():
    nifty = yf.Ticker("^NSEI")
    df = nifty.history(period="2y", interval="1h")
    df.reset_index(inplace=True)
    print(df.tail(10))

def live_data():
    nifty = yf.Ticker("^NSEI")
    df = nifty.history(period="2y", interval="1h")
    dirname = pathlib.Path(__file__).parent.resolve().parent.resolve()
    df.reset_index(inplace=True)
    df.to_csv(str(dirname)+str("/data/raw/data.csv"),index=False)
    print(df.head())

if __name__ == '__main__':
    
    if sys.argv[1]=='historic':
        historic_data()

    if sys.argv[1]=='live':
        live_data()
