import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from core.data_fetcher import get_price_data

def plot_ma_crossover(symbol: str, period="1y", short=20, long=50):
    df = get_price_data(symbol, period=period)
    if df.empty:
        return None

    # normalize column names
    for c in df.columns:
        if "Close" in c:
            df.rename(columns={c: "Close"}, inplace=True)

    # compute moving averages
    df["SMA_short"] = df["Close"].rolling(window=short).mean()
    df["SMA_long"] = df["Close"].rolling(window=long).mean()

    # buy/sell signals
    df["Signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "Signal"] = 1
    df.loc[df["SMA_short"] <= df["SMA_long"], "Signal"] = -1

    # plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Date"], df["Close"], label="Close", linewidth=1.2)
    ax.plot(df["Date"], df["SMA_short"], label=f"SMA {short}", linewidth=1)
    ax.plot(df["Date"], df["SMA_long"], label=f"SMA {long}", linewidth=1)

    # mark buys/sells
    buys = df[df["Signal"] == 1]
    sells = df[df["Signal"] == -1]
    ax.scatter(buys["Date"], buys["Close"], color="green", marker="^", s=40, label="BUY", alpha=0.7)
    ax.scatter(sells["Date"], sells["Close"], color="red", marker="v", s=40, label="SELL", alpha=0.7)

    ax.set_title(f"{symbol} {short}/{long} MA Crossover", fontsize=12)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    # stream as PNG
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig)
    return StreamingResponse(buf, media_type="image/png")
