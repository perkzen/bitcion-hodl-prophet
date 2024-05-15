import argparse

import yfinance as yf
from ..utils.logger import setup_logger


def main():
    logger = setup_logger()

    parser = argparse.ArgumentParser(description="Download historical data for BTC-USD.")

    parser.add_argument("--type", type=str, default="hourly",
                        help="Interval to download data for. Options: hourly, daily")

    args = parser.parse_args()

    valid_intervals = {"hourly", "daily"}
    if args.type not in valid_intervals:
        parser.error(f"Invalid type '{args.type}'. Valid options are: {', '.join(valid_intervals)}")

    logger.info(f"Arguments received - interval: {args.type}")

    intervals = {
        "hourly": {
            "period": "2y",
            "interval": "1h"
        },
        "daily": {
            "period": "max",
            "interval": "1d"
        }
    }

    logger.info("Downloading historical data for BTC-USD.")

    btc = yf.Ticker("BTC-USD")

    btc_hist = btc.history(period=intervals[args.type]["period"], interval=intervals[args.type]["interval"])

    btc_hist.to_csv(f"data/raw/btc_price_{args.type}.csv")


if __name__ == "__main__":
    main()
