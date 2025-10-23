from fastapi import APIRouter
from core.strategies import moving_average_crossover

router = APIRouter(prefix="/strategy", tags=["Strategy"])

@router.get("/ma_crossover/{symbol}")
def run_strategy(symbol: str, period: str = "1y", short: int = 20, long: int = 50):
    result = moving_average_crossover(symbol, period, short, long)
    return result
