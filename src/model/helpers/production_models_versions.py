from src.model.helpers.common import ModelType
from src.utils.data import DataType
from src.model.helpers.mlflow import get_model_version, Stage, mlflow_authenticate

client = mlflow_authenticate()

_daily_price_model_version = get_model_version(client=client, data_type=DataType.DAILY.value, model_name="model.onnx",
                                               stage=Stage.PRODUCTION)
_hourly_price_model_version = get_model_version(client=client, data_type=DataType.HOURLY.value, model_name="model.onnx",
                                                stage=Stage.PRODUCTION)
_daily_direction_model_version = get_model_version(client=client, data_type=DataType.DAILY.value,
                                                   model_name="cls_model.onnx", stage=Stage.PRODUCTION)
_hourly_direction_model_version = get_model_version(client=client, data_type=DataType.HOURLY.value,
                                                    model_name="cls_model.onnx", stage=Stage.PRODUCTION)


def get_production_model_version(data_type: DataType, model_type: ModelType) -> str:
    if model_type == ModelType.REGRESSION:
        return _daily_price_model_version if data_type == DataType.DAILY else _hourly_price_model_version
    elif model_type == ModelType.CLASSIFICATION:
        return _daily_direction_model_version if data_type == DataType.DAILY else _hourly_direction_model_version
    else:
        raise ValueError("Invalid model type")
