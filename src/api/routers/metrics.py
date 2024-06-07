from fastapi import APIRouter

from src.api.models.model_metric import ModelMetric
from src.api.services import metrics_service

router = APIRouter(
    tags=["Metrics"],
    prefix="/metrics"
)


@router.get("")
def find_all() -> list[ModelMetric]:
    return metrics_service.find_all()
