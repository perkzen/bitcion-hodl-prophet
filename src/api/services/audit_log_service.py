from src.api.db.client import db
from src.api.models.audit_log import AuditLog
from src.model.helpers.common import ModelType
from src.utils.data import DataType
from src.utils.logger import get_logger

_collection = db["audit_logs"]

logger = get_logger()


def save(log: AuditLog) -> str:
    result = _collection.insert_one(log.dict())
    logger.info(f"Saved audit log: {result.inserted_id}")
    return result.inserted_id


def find_all() -> list[AuditLog]:
    return [AuditLog(**log) for log in _collection.find()]


def find_by_model_type(model_type: str, data_type: str) -> list[AuditLog]:
    return [AuditLog(**log) for log in _collection.find({"model_type": model_type, "data_type": data_type})]
