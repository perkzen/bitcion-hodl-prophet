import pandas as pd
import yfinance as yf

from src.utils.data import DataType

ticker = yf.Ticker("BTC-USD")

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


def get_last_n_entries(n: int, data_type: DataType, use_data=False) -> pd.DataFrame:
    btc_hist = yf.download("BTC-USD", period=options[data_type.value]["period"],
                           interval=options[data_type.value]["interval"])
    btc_hist.drop(columns=["Adj Close"], inplace=True)

    btc_hist.columns = [col.lower() for col in btc_hist.columns]

    if use_data:
        # Reset the index to include it as a column
        btc_hist.index.rename("date", inplace=True)
        btc_hist.reset_index(inplace=True)

    # numeric cols to have only 2 decimal places
    numeric_cols = btc_hist.select_dtypes(include="number").columns

    btc_hist[numeric_cols] = btc_hist[numeric_cols].map(lambda x: round(x, 2))

    return btc_hist.tail(n)
