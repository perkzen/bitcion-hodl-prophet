import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score

from src.model.helpers import prepare_data
from src.vizualization.helpers import plot_predictions


def load_model(path: str) -> ort.InferenceSession:
    return ort.InferenceSession(path)


def predict(model: ort.InferenceSession, data: np.ndarray) -> np.ndarray:
    return model.run(["output"], {"input": data})[0]


def inverse_transform(data: np.ndarray, num_of_features: int, scaler: joblib.load) -> np.ndarray:
    data_copy = np.repeat(data, num_of_features, axis=-1)
    return scaler.inverse_transform(np.reshape(data_copy, (len(data), num_of_features)))[:, 0]


def evaluate_model_performance(y_true, y_pred) -> dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    evs = explained_variance_score(y_true, y_pred)

    return {"mse": mse, "mae": mae, "evs": evs}


def main() -> None:
    model = load_model("models/model.onnx")
    minmax = joblib.load("models/minmax.pkl")

    btc_hist = pd.read_csv("data/processed/btc_price_daily.csv", index_col=0, parse_dates=True)

    _, _, X_test, y_test = prepare_data(minmax, btc_hist)

    y_pred = predict(model, X_test)

    y_true = inverse_transform(data=y_test, num_of_features=5, scaler=minmax)
    y_pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)

    dates = btc_hist.index.values
    df_output = pd.DataFrame({"Date": dates[-len(y_true):], 'Actual': y_true, 'Predicted': y_pred})

    plot_predictions(df_output, output_file="reports/figures/predictions.png")

    print(evaluate_model_performance(y_true, y_pred))


if __name__ == '__main__':
    main()
