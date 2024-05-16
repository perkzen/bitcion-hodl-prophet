import argparse
import os
import pandas as pd
from scipy.stats import ks_2samp

from src.utils.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Kolmogorov-Smirnov test')
    parser.add_argument('--current', type=str, required=True, help='Path to current file')
    parser.add_argument('--reference', type=str, required=True, help='Path to reference data file')
    parser.add_argument('--alpha', type=float, default=0.05, help='Significance level')

    return parser


def valid_args(args) -> bool:
    files = os.listdir("data/processed")

    if args.current not in files:
        return False

    if args.reference not in files:
        return False

    return True


def main() -> None:
    logger = get_logger()
    parser = create_parser()

    args = parser.parse_args()

    valid = valid_args(args)
    if not valid:
        parser.error(
            f'Invalid input for current or reference data. Valid options are: {", ".join(os.listdir("data/processed"))}')

    logger.info(f'Arguments received - current: {args.current}, reference: {args.reference}, alpha: {args.alpha}')

    current = pd.read_csv(f'data/processed/{args.current}', index_col=0, parse_dates=True)
    reference = pd.read_csv(f'data/processed/{args.reference}', index_col=0, parse_dates=True)

    for col in current.columns:
        ks_stat, p_value = ks_2samp(current[col], reference[col])
        if p_value < args.alpha:
            raise ValueError(
                f'Kolmogorov-Smirnov test failed for {col} - distributions are different (p-value: {p_value})'
            )
        else:
            logger.info(f'Kolmogorov-Smirnov test for {col} - p-value: {p_value}, distributions are the same')


if __name__ == '__main__':
    main()
