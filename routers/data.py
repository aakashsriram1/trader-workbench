from fastapi import APIRouter
from core.data_fetcher import get_price_data

router = APIRouter(prefix="/data", tags=["Data"])

@router.get("/{symbol}")
def fetch_data(symbol: str):
    df = get_price_data(symbol)
    return df.to_dict(orient="records")
    