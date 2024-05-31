from enum import Enum

import numpy as np
import pandas as pd
import onnxruntime as ort


class ModelType(Enum):
    REGRESSION = "reg"
    CLASSIFICATION = "cls"


valid_model_types = {ModelType.REGRESSION.value, ModelType.CLASSIFICATION.value}


def create_test_train_split(data: pd.DataFrame, split_size=0.3) -> tuple[np.ndarray, np.ndarray]:
    items = int(len(data) * split_size)
    test_data = data.iloc[-items:]
    train_data = data.iloc[:-items]

    return train_data, test_data


def load_model(path: str) -> ort.InferenceSession:
    return ort.InferenceSession(path)


def predict(model: ort.InferenceSession, data: np.ndarray) -> np.ndarray:
    input_names = model.get_inputs()[0].name
    output_names = model.get_outputs()[0].name
    return model.run([output_names], {input_names: data})[0]
