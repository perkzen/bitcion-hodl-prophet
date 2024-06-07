from src.api.db.client import db
from src.api.models.model_metric import ModelMetric
from src.model.helpers.production_models_versions import daily_price_model_version, daily_direction_model_version, \
    hourly_price_model_version, hourly_direction_model_version
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
        "model_version": daily_price_model_version
    }
    daily_cls_query = {
        "model_type": "cls",
        "data_type": "daily",
        "model_version": daily_direction_model_version
    }

    hourly_reg_query = {
        "model_type": "reg",
        "data_type": "hourly",
        "model_version": hourly_price_model_version
    }

    hourly_cls_query = {
        "model_type": "cls",
        "data_type": "hourly",
        "model_version": hourly_direction_model_version
    }

    return [ModelMetric(**metric) for metric in
            _collection.find({"$or": [daily_reg_query, daily_cls_query, hourly_reg_query, hourly_cls_query]})]
