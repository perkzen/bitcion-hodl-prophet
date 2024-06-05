import onnx
import dagshub.auth
import dagshub
import joblib
import mlflow
from enum import Enum
from typing import Any
from mlflow import MlflowClient
from mlflow.onnx import log_model, load_model as load_onnx
from mlflow.models import ModelSignature
from mlflow.sklearn import log_model as log_minmax, load_model as load_minmax
from onnxruntime import InferenceSession
from sklearn.preprocessing import MinMaxScaler
from src.config import settings
from src.model.helpers.common import ModelType, load_model
from src.utils.data import DataType


class Stage(Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


def mlflow_authenticate() -> MlflowClient:
    dagshub.auth.add_app_token(token=settings.dagshub_user_token)
    dagshub.init(repo_owner='perkzen', repo_name='bitcoin-hodl-prophet', mlflow=True)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    client = MlflowClient()

    return client


def ensure_model_exists(client: MlflowClient, model_name: str):
    try:
        client.get_registered_model(model_name)
    except mlflow.exceptions.RestException as e:
        if e.error_code == 'RESOURCE_DOES_NOT_EXIST':
            client.create_registered_model(model_name)


def upload_model(client: MlflowClient, model: Any, model_name: str, signature: ModelSignature) -> None:
    ensure_model_exists(client, model_name)
    saved_model = log_model(onnx_model=model, artifact_path=f"models/{model_name}", signature=signature)
    mv = client.create_model_version(name=model_name, source=saved_model.model_uri, run_id=saved_model.run_id)
    client.set_registered_model_alias(name=model_name, alias=Stage.STAGING.value, version=mv.version)


def upload_minmax(client: MlflowClient, minmax: Any, model_name: str) -> None:
    ensure_model_exists(client, model_name)
    metadata = {"feature_range": minmax.feature_range}
    saved_minmax = log_minmax(sk_model=minmax, artifact_path=f"minmax/{model_name}", registered_model_name=model_name,
                              metadata=metadata)
    mv = client.create_model_version(name=model_name, source=saved_minmax.model_uri, run_id=saved_minmax.run_id)
    client.set_registered_model_alias(name=model_name, alias=Stage.STAGING.value, version=mv.version)


def download_model(client: MlflowClient, model_name: str, data_type: str, stage: Stage) -> str:
    model_url = client.get_model_version_by_alias(f"models/{data_type}/{model_name}", stage.value).source
    model = load_onnx(model_url)
    file_path = f"models/{data_type}/{stage.value}_{model_name}"
    onnx.save_model(model, file_path)
    return file_path


def download_minmax(client: MlflowClient, minmax_name: str, data_type: str, stage: Stage) -> str:
    minmax_url = client.get_model_version_by_alias(f"models/{data_type}/{minmax_name}", stage.value).source
    minmax = load_minmax(minmax_url)
    file_path = f"models/{data_type}/{stage.value}_{minmax_name}"
    joblib.dump(minmax, file_path)
    return file_path


def download_production_models(client: MlflowClient, model_name: str, minmax_name: str, data_type: str) -> \
        tuple[InferenceSession, MinMaxScaler] | tuple[None, None]:
    try:
        model_path = download_model(client, model_name, data_type, Stage.PRODUCTION)
        minmax_path = download_minmax(client, minmax_name, data_type, Stage.PRODUCTION)

        model = load_model(model_path)
        minmax = joblib.load(minmax_path)

        return model, minmax

    except mlflow.exceptions.RestException as e:
        if e.error_code == 'RESOURCE_DOES_NOT_EXIST' or e.error_code == 'INVALID_PARAMETER_VALUE':
            return None, None


def download_staging_models(client: MlflowClient, model_name: str, minmax_name: str, data_type: str) -> \
        tuple[InferenceSession, MinMaxScaler] | tuple[None, None]:
    try:
        model_path = download_model(client, model_name, data_type, Stage.STAGING)
        minmax_path = download_minmax(client, minmax_name, data_type, Stage.STAGING)

        model = load_model(model_path)
        minmax = joblib.load(minmax_path)

        return model, minmax

    except mlflow.exceptions.RestException as e:
        if e.error_code == 'RESOURCE_DOES_NOT_EXIST' or e.error_code == 'INVALID_PARAMETER_VALUE':
            return None, None


def promote_model(client: MlflowClient, model_name: str, minmax_name: str, data_type: str) -> None:
    model_name = f"models/{data_type}/{model_name}"
    minmax_name = f"models/{data_type}/{minmax_name}"

    staging_model = client.get_model_version_by_alias(model_name, Stage.STAGING.value)
    staging_minmax = client.get_model_version_by_alias(minmax_name, Stage.STAGING.value)

    # Promote staging model to production
    client.set_registered_model_alias(name=model_name, alias=Stage.PRODUCTION.value, version=staging_model.version)
    client.set_registered_model_alias(name=minmax_name, alias=Stage.PRODUCTION.value, version=staging_minmax.version)

    client.delete_registered_model_alias(name=model_name, alias=Stage.STAGING.value)
    client.delete_registered_model_alias(name=minmax_name, alias=Stage.STAGING.value)


def demote_model(client: MlflowClient, model_name: str, minmax_name: str, data_type: str) -> None:
    model_name = f"models/{data_type}/{model_name}"
    minmax_name = f"models/{data_type}/{minmax_name}"

    production_model = client.get_model_version_by_alias(model_name, Stage.PRODUCTION.value)
    production_minmax = client.get_model_version_by_alias(minmax_name, Stage.PRODUCTION.value)

    # Demote production model to development
    client.set_registered_model_alias(name=model_name, alias=Stage.DEVELOPMENT.value, version=production_model.version)
    client.set_registered_model_alias(name=minmax_name, alias=Stage.DEVELOPMENT.value,
                                      version=production_minmax.version)

    client.delete_registered_model_alias(name=model_name, alias=Stage.PRODUCTION.value)
    client.delete_registered_model_alias(name=minmax_name, alias=Stage.PRODUCTION.value)
