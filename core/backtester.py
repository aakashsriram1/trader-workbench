import numpy as np 
from core.data_fetcher import get_price_data

def simple_backtest(symbol: str, period = "1y"):
        df = get_price_data(symbol, period=period)
        if df.empty:
            return {"symbol": symbol, "error": "no data"}

        start_price = float(df.iloc[0]["Open_" + symbol])
        end_price   = float(df.iloc[-1]["Close_" + symbol])
        change_pct  = (end_price / start_price - 1) * 100
        
        # Daily returns
        closes = df["Close_" + symbol].values
        daily_returns = np.diff(closes) / closes[:-1]
        cagr = ((1 + daily_returns.mean()) ** 252 - 1) * 100  # assume 252 trading days

        return {
            "symbol": symbol,
            "start_price": start_price,
            "end_price": end_price,
            "total_return_%": round(change_pct, 2),
            "annualized_return_%": round(cagr, 2),
        }