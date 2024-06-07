from src.api.db.client import db
from src.api.models.model_metric import ModelMetric
from src.model.helpers.common import ModelType
from src.model.helpers.production_models_versions import get_production_model_version
from src.utils.data import DataType
from src.utils.logger import get_logger

_collection = db["model_metrics"]

logger = get_logger()


def save(metric: ModelMetric) -> str:
    result = _collection.insert_one(metric.dict())
    logger.info(f"Saved model metric: {result.inserted_id}")
    return result.inserted_id


def find_all() -> list[ModelMetric]:
    daily_reg_query = {
        "model_type": "reg",
        "data_type": "daily",
        "model_version": get_production_model_version(DataType.DAILY, ModelType.REGRESSION)
    }
    daily_cls_query = {
        "model_type": "cls",
        "data_type": "daily",
        "model_version": get_production_model_version(DataType.DAILY, ModelType.CLASSIFICATION)
    }

    hourly_reg_query = {
        "model_type": "reg",
        "data_type": "hourly",
        "model_version": get_production_model_version(DataType.HOURLY, ModelType.REGRESSION)
    }

    hourly_cls_query = {
        "model_type": "cls",
        "data_type": "hourly",
        "model_version": get_production_model_version(DataType.HOURLY, ModelType.CLASSIFICATION)
    }

    daily_reg_metrics = _collection.find(daily_reg_query)
    daily_cls_metrics = _collection.find(daily_cls_query)
    hourly_reg_metrics = _collection.find(hourly_reg_query)
    hourly_cls_metrics = _collection.find(hourly_cls_query)

    return [ModelMetric(**metric) for metric in daily_reg_metrics] + \
        [ModelMetric(**metric) for metric in daily_cls_metrics] + \
        [ModelMetric(**metric) for metric in hourly_reg_metrics] + \
        [ModelMetric(**metric) for metric in hourly_cls_metrics]
