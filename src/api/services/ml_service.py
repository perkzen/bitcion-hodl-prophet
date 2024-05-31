import joblib
from src.model.helpers.regression.model import load_model, predict, create_time_series, inverse_transform
from src.utils.data import DataType
from src.api.services import btc_service


def forecast(data_type: DataType):
    model = load_model(f"models/{data_type.value}/model.onnx")
    minmax = joblib.load(f"models/{data_type.value}/minmax.pkl")

    btc_hist = btc_service.get_last_n_entries(25, data_type)

    target = "Close"
    features = list(btc_hist.columns)

    target_idx = btc_hist.columns.get_loc(target)
    feature_idx = [btc_hist.columns.get_loc(feature) for feature in features]

    data = minmax.transform(btc_hist)

    X, _ = create_time_series(data, 24, target_idx, feature_idx)

    y_pred = predict(model, X)

    pred = inverse_transform(data=y_pred, num_of_features=5, scaler=minmax)[0]

    return pred
