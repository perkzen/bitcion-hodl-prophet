import argparse
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score, accuracy_score
from src.api.models.audit_log import AuditLog
from src.api.models.model_metric import ModelMetric
from src.api.services import audit_log_service, metrics_service
from src.utils.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a model to predict the price of Bitcoin")
    parser.add_argument("--type", required=True, type=str, help="data type (daily or hourly)")
    parser.add_argument("--model", required=True, type=str, help="model type (cls or reg)")
    return parser


def valid_args(args) -> list[str]:
    errors = []

    if args.type not in {"daily", "hourly"}:
        errors.append(f"Invalid data type '{args.type}'. Valid options are: daily, hourly")
        return errors

    if args.model not in {"cls", "reg"}:
        errors.append(f"Invalid model type '{args.model}'. Valid options are: cls, reg")
        return errors

    return errors


logger = get_logger()


def validate_classification_predictions(data: pd.DataFrame, predictions: list[AuditLog]) -> None:
    actuals = []
    preds = []

    for p in predictions:
        p = p.dict()
        direction = p["prediction"]["direction"]
        prediction = 1 if direction == "up" else 0
        date = p["prediction"]["date"]
        date = pd.to_datetime(date).tz_localize('UTC')

        row = data.loc[data.index == date]
        if row.empty:
            logger.info(f"Prediction for date {date} not found")
            continue

        actual = row["target"].values[0]

        actuals.append(actual)
        preds.append(prediction)

    accuracy = accuracy_score(actuals, preds)
    precision = precision_score(actuals, preds)
    recall = recall_score(actuals, preds)
    f1 = f1_score(actuals, preds)

    logger.info(f"Accuracy: {accuracy:.2f}")
    logger.info(f"Precision: {precision:.2f}")
    logger.info(f"Recall: {recall:.2f}")
    logger.info(f"F1 Score: {f1:.2f}")

    metrics_service.save(ModelMetric(model_type="cls", data_type="hourly", model_version="1.0",
                                     metrics={"accuracy": accuracy, "precision": precision, "recall": recall,
                                              "f1": f1}))


def validate_regression_predictions(data: pd.DataFrame, predictions: list[AuditLog]) -> None:
    actuals = []
    preds = []

    for p in predictions:
        p = p.dict()
        predicted_price = p["prediction"]["price"]
        date = p["prediction"]["date"]
        date = pd.to_datetime(date).tz_localize('UTC')

        test_date = "2024-06-05 00:00:00+00:00"
        row = data.loc[data.index == test_date]
        if row.empty:
            logger.info(f"Prediction for date {date} not found")
            continue

        actual_price = row["target"].values[0]

        actuals.append(actual_price)
        preds.append(predicted_price)

    mae = mean_absolute_error(actuals, preds)
    mse = mean_squared_error(actuals, preds)
    evs = explained_variance_score(actuals, preds)

    logger.info(f"Mean Absolute Error (MAE): {mae:.2f}")
    logger.info(f"Mean Squared Error (MSE): {mse:.2f}")
    logger.info(f"Explained Variance Score (EVS): {evs:.2f}")

    metrics_service.save(ModelMetric(model_type="reg", data_type="hourly", model_version="1.0",
                                     metrics={"mae": mae, "mse": mse, "evs": evs}))


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    errors = valid_args(args)

    if errors:
        for error in errors:
            print(error)
        return

    postfix = "_classification" if args.model == "cls" else ""

    btc_hist = pd.read_csv(f"data/processed/btc_price_{args.type}{postfix}.csv", index_col=0, parse_dates=True)

    predictions = audit_log_service.find_by_model_type(args.model, args.type)

    match args.model:
        case "cls":
            validate_classification_predictions(btc_hist, predictions)
        case "reg":
            validate_regression_predictions(btc_hist, predictions)


if __name__ == '__main__':
    main()
