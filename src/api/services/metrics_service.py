from src.api.db.client import db
from src.api.models.model_metric import ModelMetric
from src.model.helpers.common import ModelType
from src.utils.data import DataType
from src.utils.logger import get_logger

_collection = db["model_metrics"]

logger = get_logger()


def save(metric: ModelMetric) -> str:
    result = _collection.insert_one(metric.dict())
    logger.info(f"Saved model metric: {result.inserted_id}")
    return result.inserted_id


def _get_query(data_type: DataType, model_type: ModelType) -> dict:
    """Generate a query dictionary for the given data and model type."""
    return {
        "model_type": model_type.value,
        "data_type": data_type.value,
    }


def find_all() -> list[ModelMetric]:
    daily_reg = find_metric(DataType.DAILY, ModelType.REGRESSION)
    daily_cls = find_metric(DataType.DAILY, ModelType.CLASSIFICATION)
    hourly_reg = find_metric(DataType.HOURLY, ModelType.REGRESSION)
    hourly_cls = find_metric(DataType.HOURLY, ModelType.CLASSIFICATION)
    return [daily_reg, daily_cls, hourly_reg, hourly_cls]


def find_metric(data_type: DataType, model_type: ModelType) -> ModelMetric:
    doc = _collection.find_one(_get_query(data_type, model_type))
    return ModelMetric(**doc)
