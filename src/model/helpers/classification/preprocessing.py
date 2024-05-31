import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.model.helpers.common import create_test_train_split


def prepare_data(minmax: MinMaxScaler, data: pd.DataFrame) \
        -> tuple[
            np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    target = "Target"
    features = [col for col in data.columns if col != target and col != "Tomorrow"]

    train_data, test_data = create_test_train_split(data)

    X_train, y_train = train_data[features], train_data[target]
    X_test, y_test = test_data[features], test_data[target]

    X_train = minmax.fit_transform(X_train)
    X_test = minmax.transform(X_test)

    return X_train, y_train, X_test, y_test
