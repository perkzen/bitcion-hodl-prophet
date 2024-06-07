from fastapi import APIRouter

from src.api.models.audit_log import AuditLog
from src.api.services import audit_log_service

router = APIRouter(
    tags=["Audit Log"],
    prefix="/audit-log"
)


@router.get("")
def find_all() -> list[AuditLog]:
    return audit_log_service.find_all()


@router.get("/{model_type}/{data_type}")
def find_by_model_type(model_type: str, data_type: str) -> list[AuditLog]:
    return audit_log_service.find_by_model_type(model_type, data_type)
