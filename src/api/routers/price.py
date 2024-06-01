from fastapi import APIRouter
from src.utils.data import DataType
from src.api.services import btc_service

router = APIRouter(
    tags=["Price"],
    prefix="/price"
)


@router.get("/{data_type}")
def get_latest_btc_price(data_type: DataType):
    data = btc_service.get_last_n_entries(-1, data_type, True)
    return data.to_dict(orient="records")
