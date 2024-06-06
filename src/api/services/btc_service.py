import pandas as pd
from src.utils.data import DataType

options = {
    DataType.HOURLY.value: {
        "period": "5d",
        "interval": "1h"
    },
    DataType.DAILY.value: {
        "period": "1mo",
        "interval": "1d"
    }
}


def get_last_n_entries(n: int, data_type: DataType) -> pd.DataFrame:
    csv_path = f"https://dagshub.com/perkzen/bitcoin-hodl-prophet/raw/main/data/processed/btc_price_{data_type.value}.csv"

    btc_hist = pd.read_csv(csv_path)
    btc_hist["date"] = pd.to_datetime(btc_hist["date"])

    # move date to last column
    btc_hist = btc_hist[[col for col in btc_hist.columns if col != "date"] + ["date"]]

    numeric_cols = btc_hist.select_dtypes(include="number").columns
    btc_hist[numeric_cols] = btc_hist[numeric_cols].round(2)

    return btc_hist.tail(n)
