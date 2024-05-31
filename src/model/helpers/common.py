import numpy as np
import pandas as pd
import onnxruntime as ort


def create_test_train_split(data: pd.DataFrame, split_size=0.3) -> tuple[np.ndarray, np.ndarray]:
    items = int(len(data) * split_size)
    test_data = data.iloc[-items:]
    train_data = data.iloc[:-items]

    return train_data, test_data


def load_model(path: str) -> ort.InferenceSession:
    return ort.InferenceSession(path)


def predict(model: ort.InferenceSession, data: np.ndarray) -> np.ndarray:
    return model.run(["output"], {"input": data})[0]
