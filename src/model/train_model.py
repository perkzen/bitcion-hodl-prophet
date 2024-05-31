import os
import argparse
import tf2onnx
import joblib
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.model.helpers.regression.model import train_model, build_model
from src.model.helpers.regression.preprocessing import prepare_data

from src.utils.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a model to predict the price of Bitcoin")
    parser.add_argument("--input", required=True, type=str, help="Path to the train data file")
    return parser


def valid_args(args) -> bool:
    files = os.listdir("data/processed")

    if args.input not in files:
        return False
    return True


def main() -> None:
    logger = get_logger()
    parser = create_parser()

    args = parser.parse_args()

    is_valid = valid_args(args)
    if not is_valid:
        parser.error(f"Invalid input '{args.input}'. Valid options are: {', '.join(os.listdir('data/processed'))}")

    logger.info(f"Training model with data from {args.input}")

    # daily or hourly
    model_type = (args.input.split("_")[2]).split(".")[0]

    data = pd.read_csv(f"data/processed/{args.input}", index_col=0, parse_dates=True)

    minmax = MinMaxScaler(feature_range=(0, 1))

    X_train, y_train, X_test, y_test = prepare_data(minmax, data)
    model = train_model(x_train=X_train, y_train=y_train, x_test=X_test, y_test=y_test, build_model_fn=build_model)

    model.output_names = ["output"]

    input_signature = [
        tf.TensorSpec(shape=(None, 24, 5), dtype=tf.double, name="input")
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

    os.makedirs(f"models/{model_type}", exist_ok=True)

    joblib.dump(minmax, f"models/{model_type}/minmax.pkl")

    with open(f"models/{model_type}/model.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())


if __name__ == '__main__':
    main()
