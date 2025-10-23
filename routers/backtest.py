from fastapi import APIRouter
from core.backtester import simple_backtest

router = APIRouter(prefix="/backtest", tags=["Backtest"])

@router.get("/{symbol}")
def run_backtest(symbol: str):
    result = simple_backtest(symbol)
    return result