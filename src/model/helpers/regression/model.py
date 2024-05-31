import numpy as np
import tensorflow_model_optimization as tfmot
import tf_keras as keras
from typing import Callable, Tuple
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
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


def evaluate_model_performance(y_true, y_pred) -> dict[str, float]:
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    evs = explained_variance_score(y_true, y_pred)

    return {"mse": mse, "mae": mae, "evs": evs}
