import argparse
import os
from logging import Logger
import mlflow
import pandas as pd
from mlflow import MlflowClient
from src.model.helpers.mlflow import mlflow_authenticate, download_staging_models, download_production_models, \
    promote_model, demote_model
from src.utils.logger import get_logger
from src.model.helpers.common import predict, ModelType, valid_model_types
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


def run_regression_evaluation(client: MlflowClient, data_type: str, logger: Logger) -> None:
    model_name = "model.onnx"
    minmax_name = "minmax.pkl"
    stg_model, stg_minmax = download_staging_models(client, model_name, minmax_name, data_type)
    prod_model, prod_minmax = download_production_models(client, model_name, minmax_name, data_type)

    if stg_model is None or stg_minmax is None:
        # we don't have a staging model because previous staging model was set to production
        logger.info("No staging model found")
        return None

    if prod_model is None or prod_minmax is None:
        # we don't need to demote the model because we don't have a production model
        promote_model(client, model_name, minmax_name, data_type)
        logger.info("No production model found, promoting staging model to production")
        return None

    btc_hist = pd.read_csv(f"data/processed/btc_price_{data_type}.csv", index_col=0, parse_dates=True)

    def make_predictions(model, minmax, data):
        _, _, X_test, y_test = prepare_reg_data(minmax, data)

        y_pred = predict(model, X_test)

        y_true = inverse_transform(data=y_test, num_of_features=5, scaler=minmax)
        y_pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)

        return y_true, y_pred

    stg_y_true, stg_y_pred = make_predictions(stg_model, stg_minmax, btc_hist)
    stg_eval = evaluate_reg_model_performance(stg_y_true, stg_y_pred)

    mlflow.log_metrics(stg_eval)

    logger.info(f"Staging model evaluation: {stg_eval}")

    prod_y_true, prod_y_pred = make_predictions(prod_model, prod_minmax, btc_hist)
    prod_eval = evaluate_reg_model_performance(prod_y_true, prod_y_pred)

    logger.info(f"Production model evaluation: {prod_eval}")

    if stg_eval["MSE"] < prod_eval["MSE"]:
        # Promote the staging model
        promote_model(client, model_name, minmax_name, data_type)
        # Demote the production model
        demote_model(client, model_name, minmax_name, data_type)
        logger.info("Staging model is better, promoting to production")
    else:
        logger.info("Production model is better, no changes needed")


def run_classification_evaluation(client: MlflowClient, data_type: str, logger: Logger) -> None:
    model_name = "cls_model.onnx"
    minmax_name = "cls_minmax.pkl"
    stg_model, stg_minmax = download_staging_models(client, model_name, minmax_name, data_type)
    prod_model, prod_minmax = download_production_models(client, model_name, minmax_name, data_type)

    if stg_model is None or stg_minmax is None:
        # we don't have a staging model because previous staging model was set to production
        logger.info("No staging model found")
        return None

    if prod_model is None or prod_minmax is None:
        # we don't need to demote the model because we don't have a production model
        promote_model(client, model_name, minmax_name, data_type)
        logger.info("No production model found, promoting staging model to production")
        return None

    btc_hist = pd.read_csv(f"data/processed/btc_price_{data_type}_classification.csv", index_col=0, parse_dates=True)

    def make_predictions(model, minmax, data):
        _, _, X_test, y_test = prepare_cls_data(minmax, data)

        y_pred = predict(model, X_test.astype(float))

        y_true = data["target"].values[-len(y_pred):]

        return y_true, y_pred

    stg_y_true, stg_y_pred = make_predictions(stg_model, stg_minmax, btc_hist)
    stg_eval = evaluate_cls_model_performance(stg_y_true, stg_y_pred)

    mlflow.log_metrics(stg_eval)

    logger.info(f"Staging model evaluation: {stg_eval}")

    prod_y_true, prod_y_pred = make_predictions(prod_model, prod_minmax, btc_hist)
    prod_eval = evaluate_cls_model_performance(prod_y_true, prod_y_pred)

    logger.info(f"Production model evaluation: {prod_eval}")

    if stg_eval["F1"] > prod_eval["F1"]:
        # Promote the staging model
        promote_model(client, model_name, minmax_name, data_type)
        # Demote the production model
        demote_model(client, model_name, minmax_name, data_type)
        logger.info("Staging model is better, promoting to production")
    else:
        logger.info("Production model is better, no changes needed")


def main() -> None:
    logger = get_logger()
    parser = create_parser()

    args = parser.parse_args()

    is_valid = valid_args(args)
    if not is_valid:
        parser.error(f"Invalid input '{args.type}'. Valid options are: {', '.join(os.listdir('models'))}")

    logger.info(f"Evaluating model with type '{args.model}' and data type '{args.type}'")

    client = mlflow_authenticate()

    mlflow.start_run(run_name=f"bitcoin-hodl-{args.type}-{args.model}-model")

    match args.model:
        case ModelType.REGRESSION.value:
            run_regression_evaluation(client, args.type, logger)
        case ModelType.CLASSIFICATION.value:
            run_classification_evaluation(client, args.type, logger)

    mlflow.end_run()


if __name__ == '__main__':
    main()
