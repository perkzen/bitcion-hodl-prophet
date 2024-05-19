from fastapi import APIRouter

from src.api.services import ml_service
from src.utils.data import DataType

router = APIRouter(
    tags=["predict"],
    prefix="/predict"
)


@router.get("/{data_type}")
def predict(data_type: DataType):
    prediction = ml_service.forecast(data_type)

    return {"prediction": float(prediction)}
