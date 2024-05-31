import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.model.helpers.common import create_test_train_split


def create_time_series(data, n_past, target_col=0, feature_cols=None):
    if feature_cols is None:
        feature_cols = list(range(data.shape[1]))

    X, y = [], []
    for i in range(n_past, len(data)):
        X.append(data[i - n_past:i, feature_cols])
        y.append(data[i, target_col])

    return np.array(X), np.array(y)


def prepare_data(minmax: MinMaxScaler, data: pd.DataFrame, n_past=24) \
        -> tuple[
            np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    target = "Close"
    features = list(data.columns)

    target_idx = data.columns.get_loc(target)
    feature_idx = [data.columns.get_loc(feature) for feature in features]

    train_data, test_data = create_test_train_split(data)

    train_data = minmax.fit_transform(train_data)
    test_data = minmax.transform(test_data)

    X_train, y_train = create_time_series(train_data, n_past, target_idx, feature_idx)
    X_test, y_test = create_time_series(test_data, n_past, target_idx, feature_idx)

    return X_train, y_train, X_test, y_test


def inverse_transform(data: np.ndarray, num_of_features: int, scaler: MinMaxScaler) -> np.ndarray:
    data_copy = np.repeat(data, num_of_features, axis=-1)
    return scaler.inverse_transform(np.reshape(data_copy, (len(data), num_of_features)))[:, 0]
