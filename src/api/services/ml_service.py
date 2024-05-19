import joblib
import pandas as pd

from src.model.helpers import load_model, predict, create_time_series, inverse_transform
from src.utils.data import DataType


def forecast(data_type: DataType):
    model = load_model(f"models/{data_type.value}/model.onnx")
    minmax = joblib.load(f"models/{data_type.value}/minmax.pkl")

    btc_hist = pd.read_csv(f"data/processed/btc_price_{data_type.value}.csv", index_col=0, parse_dates=True)

    btc_hist = btc_hist.iloc[-25:]

    target = "Close"
    features = list(btc_hist.columns)

    target_idx = btc_hist.columns.get_loc(target)
    feature_idx = [btc_hist.columns.get_loc(feature) for feature in features]

    data = minmax.transform(btc_hist)

    X, _ = create_time_series(data, 24, target_idx, feature_idx)

    y_pred = predict(model, X)

    pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)[0]

    return pred
