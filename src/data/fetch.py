import argparse
import pandas as pd
import yfinance as yf
from src.utils.data import DataType
from src.utils.logger import get_logger

valid_intervals = {DataType.HOURLY.value, DataType.DAILY.value}

options = {
    DataType.HOURLY.value: {
        "period": "1d",
        "interval": "1h"
    },
    DataType.DAILY.value: {
        "period": "1d",
        "interval": "1d"
    }
}


def valid_args(args) -> bool:
    if args.type not in valid_intervals:
        return False
    return True


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download historical data for BTC-USD.")
    parser.add_argument("--type", type=str, default="hourly",
                        help="Interval to download data for. Options: hourly, daily")

    return parser


def main() -> None:
    logger = get_logger()
    parser = create_parser()
    args = parser.parse_args()

    is_valid = valid_args(args)
    if not is_valid:
        parser.error(f"Invalid type '{args.type}'. Valid options are: {', '.join(valid_intervals)}")

    logger.info(f"Arguments received - interval: {args.type}")
    logger.info("Downloading historical data for BTC-USD.")

    btc = yf.Ticker("BTC-USD")

    current_btc_price = btc.history(period=options[args.type]["period"], interval=options[args.type]["interval"])
    btc_price_hist = pd.read_csv(f"data/raw/btc_price_{args.type}.csv", index_col=0, parse_dates=True)

    btc_price_hist = pd.concat([btc_price_hist, current_btc_price]).sort_index()

    btc_price_hist = btc_price_hist[~btc_price_hist.index.duplicated(keep='first')]

    btc_price_hist.to_csv(f"data/raw/btc_price_{args.type}.csv")


if __name__ == "__main__":
    main()
