from fastapi import APIRouter
from src.api.services import forecast_service
from src.utils.data import DataType

router = APIRouter(
    tags=["predict"],
    prefix="/predict"
)


@router.get("/price/{data_type}")
def predict_price(data_type: DataType):
    prediction = forecast_service.forecast_price(data_type)
    return {"prediction": float(prediction)}


@router.get("/direction/{data_type}")
def predict_direction(data_type: DataType):
    prediction = forecast_service.forecast_direction(data_type)
    return {"prediction": "up" if prediction > 0 else "down"}
