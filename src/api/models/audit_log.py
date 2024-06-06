from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, timezone
from typing import Any, Dict


class AuditLog(BaseModel):
    model_type: str
    data_type: str
    model_version: str
    prediction: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    @field_validator('created_at', mode='before')
    def set_created_at(cls, value):
        return value or datetime.now(timezone.utc)

    model_config = ConfigDict(protected_namespaces=())
