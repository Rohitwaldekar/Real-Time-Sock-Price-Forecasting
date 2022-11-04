# import requests
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json
# import pandas as pd

# import os
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv('APCA_API_KEY_ID')
# api_secret = os.getenv('APCA_API_SECRET_KEY')

# url = 'https://paper-api.alpaca.markets'
# api_call = '/v2/assets/:APPL'

# headers = {'content-type': 'application/json', 
#            'Apca-Api-Key-Id': api_key, 
#            'Apca-Api-Secret-Key': api_secret}

# response = requests.get(url + api_call, headers=headers)
# response = json.loads(response.text)
# print(response)
# assets = [dict(item) for item in response]
# df = pd.DataFrame.from_records(assets)
# print(df.head())
###################################################################################################
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('APCA_API_KEY_ID')
api_secret = os.getenv('APCA_API_SECRET_KEY')

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockLatestBarRequest
from alpaca.data.timeframe import TimeFrame
# from alpaca.data import StockDataStream
# from alpaca.data.live import StockDataStream

# keys required
client = StockHistoricalDataClient(api_key, api_secret)
# stock_stream = StockDataStream(api_key, api_secret)

# multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY", "GLD", "TLT"])
# request_params = StockLatestBarRequest(
#                         symbol_or_symbols=["SPY", "GLD", "TLT"],
#                         timeframe=TimeFrame.Hour,
#                         start="2022-07-01"
#                  )

# bars = client.get_stock_bars(request_params)
# bars.df
# gld_latest_ask_price = bars["GLD"]

# latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)

# gld_latest_ask_price = latest_multisymbol_quotes["GLD"]

# print(gld_latest_ask_price)


'''
# async handler
async def quote_data_handler(data: any):
    # quote data will arrive here
    print(data)

stock_stream.subscribe_quotes(quote_data_handler, "SPY")

stock_stream.run()
'''

# from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.historical import StockHistoricalDataClient
# from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.requests import StockBarsRequest
# from alpaca.data.timeframe import TimeFrame

# no keys required for crypto data
client = StockHistoricalDataClient(api_key, api_secret)

request_params = StockBarsRequest(
                        symbol_or_symbols=["SPY", "GLD", "TLT"],
                        timeframe=TimeFrame.Hour,
                        start="2022-11-01 00:00:00",
                        end="2022-11-02 00:00:00"
                 )

bars = client.get_stock_bars(request_params)

# convert to dataframe
bars.df

# access bars as list - important to note that you must access by symbol key
# even for a single symbol request - models are agnostic to number of symbols
print(bars["GLD"])