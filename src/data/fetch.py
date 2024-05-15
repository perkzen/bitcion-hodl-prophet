import argparse
import yfinance as yf
from enum import Enum
from src.utils.logger import get_logger


class Type(Enum):
    HOURLY = "hourly"
    DAILY = "daily"


valid_intervals = {Type.HOURLY.value, Type.DAILY.value}

options = {
    Type.HOURLY: {
        "period": "2y",
        "interval": "1h"
    },
    Type.DAILY: {
        "period": "max",
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
    btc_hist = btc.history(period=options[args.type]["period"], interval=options[args.type]["interval"])
    btc_hist.to_csv(f"data/raw/btc_price_{args.type}.csv")


if __name__ == "__main__":
    main()
