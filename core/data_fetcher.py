import yfinance as yf
import pandas as pd

def get_price_data(symbol: str, period="1y", interval="1d"):
    # Fetch data correctly for the given period
    data = yf.download(
        tickers=symbol,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=True  # helps remove dividends/splits adjustments
    )

    # Flatten columns if multi-index
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]

    data.reset_index(inplace=True)
    return data
