import pandas as pd

from src.api.services import btc_service
from src.utils.data import DataType


def test_daily_btc_service():
    data = btc_service.get_last_n_entries(24, DataType.DAILY)
    last_date = data.index[-1].date()
    current_date = pd.Timestamp.now().date()

    assert last_date == current_date
    assert len(data) == 24


def test_hourly_btc_service():
    data = btc_service.get_last_n_entries(24, DataType.HOURLY)
    last_date = data.index[-1].date()
    current_date = pd.Timestamp.now().date()

    assert last_date == current_date
    assert len(data) == 24
