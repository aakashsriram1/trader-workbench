import numpy as np
import pandas as pd
from core.data_fetcher import get_price_data

def moving_average_crossover(symbol: str, period="1y", short=20, long=50):
    df = get_price_data(symbol, period=period)
    print(df.columns)
    print(df.head())


    if df.empty:
        return {"symbol": symbol, "error": "no data"}

    # --- Normalize column names ---
    # Example: "Close_AAPL" → "Close"
    rename_map = {}
    for col in df.columns:
        if "Close" in col: rename_map[col] = "Close"
        if "Open" in col:  rename_map[col] = "Open"
        if "High" in col:  rename_map[col] = "High"
        if "Low" in col:   rename_map[col] = "Low"
        if "Volume" in col:rename_map[col] = "Volume"
    df.rename(columns=rename_map, inplace=True)

    # Double-check: if "Close" still missing, bail early
    if "Close" not in df.columns:
        return {"symbol": symbol, "error": f"unexpected columns: {list(df.columns)}"}

    # --- Strategy logic ---
    df["SMA_short"] = df["Close"].rolling(window=short).mean()
    df["SMA_long"] = df["Close"].rolling(window=long).mean()

    df["Signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "Signal"] = 1  # buy
    df["Daily_Return"] = df["Close"].pct_change()
    df["Strategy_Return"] = df["Signal"].shift(1) * df["Daily_Return"]

    total_return = (df["Strategy_Return"] + 1).prod() - 1
    cagr = ((1 + df["Strategy_Return"].mean()) ** 252 - 1)

    return {
        "symbol": symbol,
        "short_window": short,
        "long_window": long,
        "total_return_%": round(total_return * 100, 2),
        "annualized_return_%": round(cagr * 100, 2),
        "last_signal": "BUY" if df.iloc[-1]["Signal"] == 1 else "SELL"
    }
