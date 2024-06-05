from src.model.helpers.mlflow import mlflow_authenticate, download_production_models
from src.utils.logger import get_logger


def main() -> None:
    logger = get_logger()

    client = mlflow_authenticate()

    # Regression models
    download_production_models(client, "model.onnx", "minmax.pkl", "daily")
    download_production_models(client, "model.onnx", "minmax.pkl", "hourly")
    logger.info("Downloaded regression production models")

    # Classification models
    download_production_models(client, "cls_model.onnx", "cls_minmax.pkl", "daily")
    download_production_models(client, "cls_model.onnx", "cls_minmax.pkl", "hourly")
    logger.info("Downloaded classification production models")


if __name__ == "__main__":
    main()
