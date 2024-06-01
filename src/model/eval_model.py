import argparse
import os
import joblib
import pandas as pd
from src.utils.logger import get_logger
from src.vizualization.helpers import plot_predictions
from src.model.helpers.common import load_model, predict, ModelType, valid_model_types
from src.model.helpers.regression.model import evaluate_model_performance as evaluate_reg_model_performance
from src.model.helpers.regression.preprocessing import inverse_transform, prepare_data as prepare_reg_data
from src.model.helpers.classification.model import evaluate_model_performance as evaluate_cls_model_performance
from src.model.helpers.classification.preprocessing import prepare_data as prepare_cls_data


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate the model to predict the price of Bitcoin")
    parser.add_argument("--type", required=True, type=str, help="model type (daily or hourly)")
    parser.add_argument("--model", required=True, type=str, help="model type (cls or reg)")
    return parser


def valid_args(args) -> bool:
    files = os.listdir("models")

    if args.type not in files:
        return False

    if args.model not in valid_model_types:
        return False

    return True


def run_regression_evaluation(data_type: str) -> None:
    model = load_model(f"models/{data_type}/model.onnx")
    minmax = joblib.load(f"models/{data_type}/minmax.pkl")

    btc_hist = pd.read_csv(f"data/processed/btc_price_{data_type}.csv", index_col=0, parse_dates=True)

    _, _, X_test, y_test = prepare_reg_data(minmax, btc_hist)

    y_pred = predict(model, X_test)

    y_true = inverse_transform(data=y_test, num_of_features=5, scaler=minmax)
    y_pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)

    dates = btc_hist.index.values
    df_output = pd.DataFrame({"Date": dates[-len(y_true):], 'Actual': y_true, 'Predicted': y_pred})

    plot_predictions(df_output, output_file=f"reports/figures/predictions_{data_type}.png")

    print(evaluate_reg_model_performance(y_true, y_pred))


def run_classification_evaluation(data_type: str) -> None:
    model = load_model(f"models/{data_type}/cls_model.onnx")
    minmax = joblib.load(f"models/{data_type}/cls_minmax.pkl")

    btc_hist = pd.read_csv(f"data/processed/btc_price_{data_type}_classification.csv", index_col=0, parse_dates=True)

    _, _, X_test, y_test = prepare_cls_data(minmax, btc_hist)

    y_pred = predict(model, X_test.astype(float))

    y_true = btc_hist["target"].values[-len(y_pred):]

    print(evaluate_cls_model_performance(y_true, y_pred))


def main() -> None:
    logger = get_logger()
    parser = create_parser()

    args = parser.parse_args()

    is_valid = valid_args(args)
    if not is_valid:
        parser.error(f"Invalid input '{args.type}'. Valid options are: {', '.join(os.listdir('models'))}")

    logger.info(f"Evaluating model with type '{args.model}' and data type '{args.type}'")

    match args.model:
        case ModelType.REGRESSION.value:
            run_regression_evaluation(args.type)
        case ModelType.CLASSIFICATION.value:
            run_classification_evaluation(args.type)


if __name__ == '__main__':
    main()
