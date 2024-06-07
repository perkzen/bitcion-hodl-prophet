import pandas as pd
import yfinance as yf
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

btc = yf.Ticker("BTC-USD")


def get_price_history(n: int, data_type: DataType) -> pd.DataFrame:
    btc_hist = btc.history(period=options[data_type.value]["period"], interval=options[data_type.value]["interval"])

    features = ["open", "high", "low", "close", "volume"]

    # col to lower case
    btc_hist.columns = btc_hist.columns.str.lower()

    btc_hist = btc_hist[features]

    # use date from index
    btc_hist["date"] = btc_hist.index

    return btc_hist.tail(n)
