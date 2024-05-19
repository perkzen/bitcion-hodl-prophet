import pandas as pd

from src.vizualization.helpers import plot_values


def main() -> None:
    df = pd.read_csv("data/processed/btc_price_daily.csv", parse_dates=['Date'])
    plot_values(df, 'Date', 'Close', output_file="reports/figures/close_vs_date.png")


if __name__ == '__main__':
    main()
