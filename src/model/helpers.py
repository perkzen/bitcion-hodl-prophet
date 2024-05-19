from typing import Callable, Tuple
import numpy as np
import pandas as pd
import tensorflow_model_optimization as tfmot
import onnxruntime as ort
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
from sklearn.preprocessing import MinMaxScaler
import tf_keras as keras
from tensorflow_model_optimization.python.core.quantization.keras.default_8bit import default_8bit_quantize_scheme

quantize_layer = tfmot.quantization.keras.quantize_annotate_layer


def build_model(input_shape: tuple[int, int]) -> keras.Sequential:
    model = keras.Sequential(name="model")

    model.add(keras.layers.GRU(128, activation='relu', input_shape=input_shape, return_sequences=True))
    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dropout(0.2)))

    model.add(keras.layers.GRU(64, activation='relu', return_sequences=True))
    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dropout(0.2)))

    model.add(keras.layers.GRU(32, activation='relu', return_sequences=True))
    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dropout(0.2)))

    model.add(keras.layers.GRU(32, activation='relu'))

    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dense(64, activation='relu')))
    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dropout(0.2)))

    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dense(32, activation='relu')))
    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dropout(0.2)))

    model.add(tfmot.quantization.keras.quantize_annotate_layer(keras.layers.Dense(1)))

    model = tfmot.quantization.keras.quantize_apply(
        model,
        scheme=default_8bit_quantize_scheme.Default8BitQuantizeScheme(),
        quantized_layer_name_prefix='quant_'
    )

    model.compile(optimizer="adam", loss="mean_squared_error")

    return model


def train_model(x_train: np.ndarray, y_train: np.ndarray, x_test: np.ndarray, y_test: np.ndarray,
                build_model_fn: Callable[[Tuple[int, int]], keras.Sequential], epochs: int = 10, batch_size=64,
                verbose: int = 1) -> keras.Sequential:
    model = build_model_fn((x_train.shape[1], x_train.shape[2]))
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), verbose=verbose)

    return model


def create_time_series(data, n_past, target_col=0, feature_cols=None):
    if feature_cols is None:
        feature_cols = list(range(data.shape[1]))

    X, y = [], []
    for i in range(n_past, len(data)):
        X.append(data[i - n_past:i, feature_cols])
        y.append(data[i, target_col])

    return np.array(X), np.array(y)


def create_test_train_split(data: pd.DataFrame, split_size=0.3) -> tuple[np.ndarray, np.ndarray]:
    items = int(len(data) * split_size)
    test_data = data.iloc[-items:]
    train_data = data.iloc[:-items]

    return train_data, test_data


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
