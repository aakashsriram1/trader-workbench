import yfinance as yf
import pandas as pd 

def get_price_data(symbol: str, period = "1y", interval = 'id'): 
    data = yf.download(symbol,period,interval)
    data.reset_index(inplace = True)
    return data.tail(5)


print(get_price_data("APPL"))