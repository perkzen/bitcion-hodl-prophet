import pandas as pd
import yfinance as yf

from src.utils.data import DataType

ticker = yf.Ticker("BTC-USD")

options = {
    DataType.HOURLY.value: {
        "period": "2d",
        "interval": "1h"
    },
    DataType.DAILY.value: {
        "period": "30d",
        "interval": "1d"
    }
}


def get_last_n_entries(n: int, data_type: DataType) -> pd.DataFrame:
    btc_hist = yf.download("BTC-USD", period=options[data_type.value]["period"],
                           interval=options[data_type.value]["interval"])
    return btc_hist.tail(n)
