from src.api.services import btc_service
from src.utils.data import DataType


def test_daily_btc_service():
    data = btc_service.get_last_n_entries(24, DataType.DAILY)

    assert len(data) == 24


def test_hourly_btc_service():
    data = btc_service.get_last_n_entries(24, DataType.HOURLY)

    assert len(data) == 24


def test_get_max_rows():
    data = btc_service.get_last_n_entries(-1, DataType.HOURLY)

    assert len(data) > 0
