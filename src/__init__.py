# Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

import os
import sys
from dotenv import load_dotenv
import pandas as pd
import pathlib

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockLatestBarRequest
from alpaca.data.timeframe import TimeFrame
# from alpaca.data import StockDataStream
# from alpaca.data.live import StockDataStream

import yfinance as yf

'''
# async handler
async def quote_data_handler(data: any):
    # quote data will arrive here
    print(data)

stock_stream.subscribe_quotes(quote_data_handler, "SPY")

stock_stream.run()
'''

load_dotenv()

api_key = os.getenv('APCA_API_KEY_ID')
api_secret = os.getenv('APCA_API_SECRET_KEY')

# no keys required for crypto data
client = StockHistoricalDataClient(api_key, api_secret)

request_params = StockBarsRequest(
                        symbol_or_symbols=["AAPL"],                #["SPY", "GLD", "TLT"],
                        timeframe=TimeFrame.Hour,
                        start="2022-08-01 00:00:00",
                        end="2022-11-01 00:00:00"
                 )

bars = client.get_stock_bars(request_params)
# print("1.",bars)
# convert to dataframe
# bars.df
# d = bars["AAPL"]
# print("1.",d.df)
# access bars as list - important to note that you must access by symbol key
# even for a single symbol request - models are agnostic to number of symbols
# print(bars["GLD"])

assets = [dict(item) for item in bars["AAPL"]]
df = pd.DataFrame.from_records(assets)

def historic_data():
    # path = pathlib.Path('D:\DataScience\Real-Time-Data-Analysis\data\\raw\data.csv')
    # data = pd.read_csv(path)
    # final = pd.concat([data, df], ignore_index=True)
    # final.to_csv(path,index=False)
    # print(final.tail(10))
    nifty = yf.Ticker("^NSEI")
    df = nifty.history(period="2y", interval="1h")
    df.reset_index(inplace=True)
    print(df.tail(10))

def live_data():
    # print('Live') ^NSEI
    # df = yf.download(tickers = "^NSEI", start="2020-12-21", end="2022-12-20" ,interval="1h", )
    nifty = yf.Ticker("^NSEI")
    df = nifty.history(period="2y", interval="1h")
    path = pathlib.Path('D:\DataScience\Real-Time-Data-Analysis\data\\raw\data.csv')
    data = pd.read_csv(path)
    df.reset_index(inplace=True)
    # final = pd.concat([data, df], ignore_index=True)
    df.to_csv(path,index=False)
    print(df.head())

if __name__ == '__main__':
    
    if sys.argv[1]=='historic':
        historic_data()

    if sys.argv[1]=='live':
        live_data()
