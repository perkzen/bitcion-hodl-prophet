import argparse
import os
import pandas as pd

from src.utils.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Validate new (current) data against reference data.')
    parser.add_argument('--current', type=str, required=True, help='Path to current data file')
    parser.add_argument('--reference', type=str, required=True, help='Path to reference data file')

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
            f'Invalid input for current or reference data. Valid options are: {", ".join(os.listdir("data/processed"))}'
        )

    logger.info(f'Arguments received - current: {args.current}, reference: {args.reference}')

    current = pd.read_csv(f"data/processed/{args.current}", index_col=0, parse_dates=True)
    reference = pd.read_csv(f"data/processed/{args.reference}", index_col=0, parse_dates=True)

    assert reference.shape[1] == current.shape[1], 'Number of columns do not match'
    assert reference.columns.all() == current.columns.all(), 'Column names do not match'
    assert reference.dtypes.all() == current.dtypes.all(), 'Data types do not match'

    logger.info('Data validation passed.')


if __name__ == '__main__':
    main()
