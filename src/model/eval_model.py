import argparse
import os
import joblib
import pandas as pd
from src.model.helpers.common import load_model, predict
from src.model.helpers.regression.model import evaluate_model_performance
from src.model.helpers.regression.preprocessing import inverse_transform, prepare_data
from src.utils.logger import get_logger
from src.vizualization.helpers import plot_predictions


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate the model to predict the price of Bitcoin")
    parser.add_argument("--type", required=True, type=str, help="model type (daily or hourly)")
    return parser


def valid_args(args) -> bool:
    files = os.listdir("models")

    if args.type not in files:
        return False
    return True


def main() -> None:
    logger = get_logger()
    parser = create_parser()

    args = parser.parse_args()

    is_valid = valid_args(args)
    if not is_valid:
        parser.error(f"Invalid input '{args.type}'. Valid options are: {', '.join(os.listdir('models'))}")

    logger.info(f"Evaluating {args.type} model")

    model = load_model(f"models/{args.type}/model.onnx")
    minmax = joblib.load(f"models/{args.type}/minmax.pkl")

    btc_hist = pd.read_csv(f"data/processed/btc_price_{args.type}.csv", index_col=0, parse_dates=True)

    _, _, X_test, y_test = prepare_data(minmax, btc_hist)

    y_pred = predict(model, X_test)

    y_true = inverse_transform(data=y_test, num_of_features=5, scaler=minmax)
    y_pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)

    dates = btc_hist.index.values
    df_output = pd.DataFrame({"Date": dates[-len(y_true):], 'Actual': y_true, 'Predicted': y_pred})

    plot_predictions(df_output, output_file=f"reports/figures/predictions_{args.type}.png")

    print(evaluate_model_performance(y_true, y_pred))


if __name__ == '__main__':
    main()
