from fastapi import APIRouter

from src.api.models.model_metric import ModelMetric
from src.api.services import metris_service

router = APIRouter(
    tags=["Metrics"],
    prefix="/metrics"
)


@router.get("")
def find_all()-> list[ModelMetric]:
    return metris_service.find_all()


@router.get("/{model_type}/{data_type}")
def find_by_model_type(model_type: str, data_type: str) -> list[ModelMetric]:
    return metris_service.find_by_model_type(model_type, data_type)
