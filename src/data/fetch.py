import argparse

import yfinance as yf
from ..utils.logger import setup_logger


def main():
    logger = setup_logger()

    parser = argparse.ArgumentParser(description="Download historical data for BTC-USD.")

    parser.add_argument("--period", type=str, default="1d",
                        help="The period of the data (e.g., '1d', '5d', '1mo', '1y').")
    parser.add_argument("--interval", type=str, default="1h",
                        help="The interval of the data (e.g., '1m', '5m', '15m', '1h', '1d').")

    args = parser.parse_args()

    logger.info(f"Arguments received - Period: {args.period}, Interval: {args.interval}")

    logger.info("Downloading historical data for BTC-USD.")

    btc = yf.Ticker("BTC-USD")

    btc_hist = btc.history(period=args.period, interval=args.interval)

    btc_hist.to_csv("data/raw/btc.csv")


if __name__ == "__main__":
    main()
