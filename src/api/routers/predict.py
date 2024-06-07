from fastapi import APIRouter, BackgroundTasks
from src.api.models.audit_log import AuditLog
from src.api.services import forecast_service, audit_log_service
from src.model.helpers.common import ModelType
from src.model.helpers.production_models_versions import daily_price_model_version, hourly_price_model_version, \
    daily_direction_model_version, hourly_direction_model_version
from src.utils.data import DataType
from src.utils.logger import get_logger

router = APIRouter(
    tags=["Predict"],
    prefix="/predict"
)

logger = get_logger()


@router.get("/price/{data_type}")
def predict_price(data_type: DataType, background_tasks: BackgroundTasks):
    result = forecast_service.forecast_price(data_type)

    model_version = daily_price_model_version if data_type == DataType.DAILY else hourly_price_model_version

    audit_log = AuditLog(
        model_type=ModelType.REGRESSION.value,  # Replace with actual model type
        data_type=data_type.value,
        model_version=model_version,
        prediction=result
    )

    background_tasks.add_task(audit_log_service.save, audit_log)

    logger.info(f"Prediction result: {result}")

    return result


@router.get("/direction/{data_type}")
def predict_direction(data_type: DataType, background_tasks: BackgroundTasks):
    result = forecast_service.forecast_direction(data_type)

    audit_log = AuditLog(
        data_type=data_type.value,
        model_version=daily_direction_model_version if data_type == DataType.DAILY else hourly_direction_model_version,
        prediction=result,
        model_type=ModelType.CLASSIFICATION.value
    )

    background_tasks.add_task(audit_log_service.save, audit_log)

    logger.info(f"Prediction result: {result}")

    return result
