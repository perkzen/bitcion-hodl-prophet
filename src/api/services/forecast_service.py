from datetime import datetime

import joblib
import pandas as pd
import pytz

from src.model.helpers.common import load_model, predict
from src.model.helpers.regression.preprocessing import create_time_series, inverse_transform
from src.utils.data import DataType
from src.api.services import btc_service

timezone = pytz.timezone('Europe/Berlin')


def forecast_price(data_type: DataType) -> dict:
    model = load_model(f"models/{data_type.value}/production_model.onnx")
    minmax = joblib.load(f"models/{data_type.value}/production_minmax.pkl")

    btc_hist = btc_service.get_price_history(25, data_type)

    target = "close"
    features = ["open", "high", "low", "close", "volume"]

    target_idx = btc_hist.columns.get_loc(target)
    feature_idx = [btc_hist.columns.get_loc(feature) for feature in features]

    data = minmax.transform(btc_hist[features])

    X, _ = create_time_series(data, 24, target_idx, feature_idx)

    y_pred = predict(model, X)

    pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)[0]

    next_date = None
    now = pd.to_datetime(datetime.now(timezone))
    now = now.replace(minute=0, second=0, microsecond=0)

    match data_type:
        case DataType.DAILY:
            next_date = now + pd.DateOffset(days=1)
        case DataType.HOURLY:
            next_date = now + pd.DateOffset(hours=1)

    return {
        "price": float(pred),
        "date": next_date
    }


def forecast_direction(data_type: DataType) -> dict:
    model = load_model(f"models/{data_type.value}/production_cls_model.onnx")
    minmax = joblib.load(f"models/{data_type.value}/production_cls_minmax.pkl")

    # get last entry to predict the next one
    btc_hist = btc_service.get_price_history(1, data_type)
    features = ["open", "high", "low", "close", "volume"]

    data = minmax.transform(btc_hist[features])

    y_pred = predict(model, data.astype(float))

    next_date = None
    now = pd.to_datetime(datetime.now(timezone))
    now = now.replace(minute=0, second=0, microsecond=0)

    match data_type:
        case DataType.DAILY:
            next_date = now + pd.DateOffset(days=1)
        case DataType.HOURLY:
            next_date = now + pd.DateOffset(hours=1)

    direction = "up" if y_pred[0] > 0 else "down"

    return {
        "direction": direction,
        "date": next_date
    }
