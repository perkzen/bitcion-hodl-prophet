from fastapi import APIRouter
from src.api.services import audit_log_service

router = APIRouter(
    tags=["Audit Log"],
    prefix="/audit-log"
)


@router.get("/")
def find_all():
    return audit_log_service.find_all()
