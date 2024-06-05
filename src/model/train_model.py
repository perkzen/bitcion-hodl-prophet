import os
import argparse
import tf2onnx
import tensorflow as tf
import pandas as pd
from mlflow import MlflowClient
from skl2onnx import to_onnx
from sklearn.preprocessing import MinMaxScaler
from src.model.helpers.mlflow import mlflow_authenticate, upload_model, upload_minmax
from src.utils.logger import get_logger
from src.model.helpers.common import valid_model_types, ModelType
from src.model.helpers.regression.model import train_model as train_reg_model, build_model as build_reg_model
from src.model.helpers.regression.preprocessing import prepare_data as prepare_reg_data
from src.model.helpers.classification.model import train_model as train_cls_model, build_model as build_cls_model
from src.model.helpers.classification.preprocessing import prepare_data as prepare_cls_data
from mlflow.models import infer_signature


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a model to predict the price of Bitcoin")
    parser.add_argument("--input", required=True, type=str, help="Path to the train data file")
    parser.add_argument("--model", required=True, type=str, help="model type (cls or reg)")
    return parser


def valid_args(args) -> list[str]:
    errors = []
    files = os.listdir("data/processed")

    if args.model not in valid_model_types:
        errors.append(f"Invalid model type '{args.model}'. Valid options are: {', '.join(valid_model_types)}")
        return errors

    if args.input not in files:
        errors.append(f"Invalid input '{args.input}'. Valid options are: {', '.join(files)}")
        return errors

    if args.model == ModelType.CLASSIFICATION.value and not args.input.endswith("_classification.csv"):
        errors.append("Classification model requires a classification input file")
        return errors

    if args.model == ModelType.REGRESSION.value and args.input.endswith("_classification.csv"):
        errors.append("Regression model requires a regression input file")
        return errors

    return errors


def run_regression_training(client: MlflowClient, input_file: str, data_type: str) -> None:
    data = pd.read_csv(f"data/processed/{input_file}", index_col=0, parse_dates=True)

    minmax = MinMaxScaler(feature_range=(0, 1))

    X_train, y_train, X_test, y_test = prepare_reg_data(minmax, data)
    model = train_reg_model(x_train=X_train, y_train=y_train, x_test=X_test, y_test=y_test,
                            build_model_fn=build_reg_model)

    model.output_names = ["output"]

    input_signature = [
        tf.TensorSpec(shape=(None, 24, 5), dtype=tf.double, name="input")
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

    model_path = f"models/{data_type}/model.onnx"
    minmax_path = f"models/{data_type}/minmax.pkl"

    signature = infer_signature(X_test, model.predict(X_test))
    upload_model(client, onnx_model, model_path, signature)
    upload_minmax(client, minmax, minmax_path)


def run_classification_training(client: MlflowClient, input_file: str, data_type: str) -> None:
    data = pd.read_csv(f"data/processed/{input_file}", index_col=0, parse_dates=True)

    minmax = MinMaxScaler(feature_range=(0, 1))

    X_train, y_train, X_test, y_test = prepare_cls_data(minmax, data)
    model = train_cls_model(x_train=X_train, y_train=y_train,
                            build_model_fn=build_cls_model)

    onnx_model = to_onnx(model, X_train.astype(float))

    model_path = f"models/{data_type}/cls_model.onnx"
    minmax_path = f"models/{data_type}/cls_minmax.pkl"

    signature = infer_signature(X_test, model.predict(X_test))
    upload_model(client, onnx_model, model_path, signature)
    upload_minmax(client, minmax, minmax_path)


def main() -> None:
    logger = get_logger()
    parser = create_parser()

    args = parser.parse_args()

    errors = valid_args(args)
    if errors:
        for error in errors:
            parser.error(error)

    logger.info(f"Training model with data input: {args.input}, type: {args.model}")

    # daily or hourly
    data_type = (args.input.split("_")[2]).split(".")[0]
    os.makedirs(f"models/{data_type}", exist_ok=True)

    client = mlflow_authenticate()

    match args.model:
        case ModelType.CLASSIFICATION.value:
            run_classification_training(client, args.input, data_type)
        case ModelType.REGRESSION.value:
            run_regression_training(client, args.input, data_type)


if __name__ == '__main__':
    main()
