from fastapi import APIRouter
from src.utils.data import DataType
from src.api.services import btc_service

router = APIRouter(
    tags=["Price"],
    prefix="/price"
)


@router.get("/{data_type}")
def get_latest_btc_price(data_type: DataType):
    n = None
    if data_type == DataType.DAILY:
        n = 7
    elif data_type == DataType.HOURLY:
        n = 24

    data = btc_service.get_price_history(n, data_type)
    return data.to_dict(orient="records")
