import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.model.helpers import prepare_data, train_model, build_model
import tensorflow as tf
import tf2onnx
import joblib


def main() -> None:
    data = pd.read_csv("data/processed/btc_price_daily.csv", index_col=0, parse_dates=True)

    minmax = MinMaxScaler()

    X_train, y_train, X_test, y_test = prepare_data(minmax, data)
    model = train_model(x_train=X_train, y_train=y_train, x_test=X_test, y_test=y_test, build_model_fn=build_model)

    model.output_names = ["output"]

    input_signature = [
        tf.TensorSpec(shape=(None, 24, 5), dtype=tf.double, name="input")
    ]

    onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

    joblib.dump(minmax, "models/minmax.pkl")

    with open("models/model.onnx", "wb") as f:
        f.write(onnx_model.SerializeToString())


if __name__ == '__main__':
    main()
