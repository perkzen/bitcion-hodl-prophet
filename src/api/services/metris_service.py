from src.api.db.client import db
from src.api.models.model_metric import ModelMetric
from src.utils.logger import get_logger

_collection = db["model_metrics"]

logger = get_logger()


def save(metric: ModelMetric) -> str:
    result = _collection.insert_one(metric.dict())
    logger.info(f"Saved model metric: {result.inserted_id}")
    return result.inserted_id


def find_all() -> list[ModelMetric]:
    return [ModelMetric(**metric) for metric in _collection.find()]


def find_by_model_type(model_type: str, data_type: str) -> list[ModelMetric]:
    return [ModelMetric(**metric) for metric in _collection.find({"model_type": model_type, "data_type": data_type})]
