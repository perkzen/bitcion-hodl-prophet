from fastapi import APIRouter
from src.api.services import forecast_service
from src.utils.data import DataType

router = APIRouter(
    tags=["Predict"],
    prefix="/predict"
)


@router.get("/price/{data_type}")
def predict_price(data_type: DataType):
    return forecast_service.forecast_price(data_type)


@router.get("/direction/{data_type}")
def predict_direction(data_type: DataType):
    return forecast_service.forecast_direction(data_type)
