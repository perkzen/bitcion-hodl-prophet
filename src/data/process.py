import argparse
import os
import pandas as pd
from src.utils.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process historical data for BTC-USD.")
    parser.add_argument("--input", type=str, required=True,
                        help="File in raw data directory to process.")

    return parser


def valid_args(args) -> bool:
    files = os.listdir("data/raw")

    if args.input not in files:
        return False
    return True


def main() -> None:
    logger = get_logger()
    parser = create_parser()
    args = parser.parse_args()
    ROWS = 1000

    is_valid = valid_args(args)
    if not is_valid:
        parser.error(f"Invalid input '{args.input}'. Valid options are: {', '.join(os.listdir('data/raw'))}")

    logger.info(f"Processing historical data for {args.input}.")

    btc_hist = pd.read_csv(f"data/raw/{args.input}", index_col=0, parse_dates=True)

    # Dividends and Stock Splits are not relevant for BTC
    btc_hist = btc_hist.drop(columns=["Dividends", "Stock Splits"])

    # if index name is Datetime rename to date
    if btc_hist.index.name == "Datetime":
        btc_hist.index.name = "date"
    else:
        btc_hist.index.name = "date"

    # column name to lower case
    btc_hist.columns = [col.lower() for col in btc_hist.columns]

    # Only keep the last n rows
    btc_hist = btc_hist.tail(ROWS)

    btc_hist.to_csv(f"data/processed/{args.input}")

    # Process for classification
    btc_hist["tomorrow"] = btc_hist["close"].shift(-1)
    btc_hist["target"] = (btc_hist["tomorrow"] > btc_hist["close"])
    btc_hist["target"] = btc_hist["target"].astype(int)

    btc_hist.to_csv(f"data/processed/{args.input.split('.')[0]}_classification.csv")
    print(btc_hist["target"].value_counts())


if __name__ == "__main__":
    main()
