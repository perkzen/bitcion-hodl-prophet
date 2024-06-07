from src.utils.data import DataType
from src.model.helpers.mlflow import get_model_version, Stage, mlflow_authenticate

client = mlflow_authenticate()

daily_price_model_version = get_model_version(client=client, data_type=DataType.DAILY.value, model_name="model.onnx",
                                              stage=Stage.PRODUCTION)
hourly_price_model_version = get_model_version(client=client, data_type=DataType.HOURLY.value, model_name="model.onnx",
                                               stage=Stage.PRODUCTION)
daily_direction_model_version = get_model_version(client=client, data_type=DataType.DAILY.value,
                                                  model_name="cls_model.onnx", stage=Stage.PRODUCTION)
hourly_direction_model_version = get_model_version(client=client, data_type=DataType.HOURLY.value,
                                                   model_name="cls_model.onnx", stage=Stage.PRODUCTION)
