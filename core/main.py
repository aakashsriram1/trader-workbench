from fastapi import FastAPI
from routers import health, data, backtest, strategy, plot

app = FastAPI(title="Trader's Workbench")
app.include_router(health.router)
app.include_router(data.router)
app.include_router(backtest.router)
app.include_router(strategy.router)
app.include_router(plot.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Trader's Workbench API running"}
