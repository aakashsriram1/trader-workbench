from fastapi import APIRouter
from core.plotter import plot_ma_crossover

router = APIRouter(prefix="/strategy", tags=["Plot"])

@router.get("/plot/{symbol}")
def plot_strategy(symbol: str, period: str = "1y", short: int = 20, long: int = 50):
    return plot_ma_crossover(symbol, period, short, long)