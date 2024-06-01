import joblib
from src.model.helpers.common import load_model, predict
from src.model.helpers.regression.preprocessing import create_time_series, inverse_transform
from src.utils.data import DataType
from src.api.services import btc_service


def forecast_price(data_type: DataType):
    model = load_model(f"models/{data_type.value}/model.onnx")
    minmax = joblib.load(f"models/{data_type.value}/minmax.pkl")

    btc_hist = btc_service.get_last_n_entries(25, data_type)

    target = "close"
    features = list(btc_hist.columns)

    target_idx = btc_hist.columns.get_loc(target)
    feature_idx = [btc_hist.columns.get_loc(feature) for feature in features]

    data = minmax.transform(btc_hist)

    X, _ = create_time_series(data, 24, target_idx, feature_idx)

    y_pred = predict(model, X)

    pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)[0]

    return pred


def forecast_direction(data_type: DataType) -> int:
    model = load_model(f"models/{data_type.value}/cls_model.onnx")
    minmax = joblib.load(f"models/{data_type.value}/cls_minmax.pkl")

    btc_hist = btc_service.get_last_n_entries(24, data_type)

    data = minmax.transform(btc_hist)

    y_pred = predict(model, data.astype(float))

    return int(y_pred[0])
