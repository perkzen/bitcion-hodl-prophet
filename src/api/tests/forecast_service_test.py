import numpy as np
from src.api.services import forecast_service
from src.utils.data import DataType


def test_hourly_price_forecast():
    predictions = forecast_service.forecast_price(data_type=DataType.HOURLY)

    assert predictions > 0
    assert isinstance(predictions, np.float32)
    assert predictions < 100_000


def test_daily_price_forecast():
    predictions = forecast_service.forecast_price(data_type=DataType.DAILY)

    assert predictions > 0
    assert isinstance(predictions, np.float32)
    assert predictions < 100_000


def test_hourly_direction_forecast():
    predictions = forecast_service.forecast_direction(data_type=DataType.HOURLY)

    assert predictions == 1 or predictions == 0


def test_daily_direction_forecast():
    predictions = forecast_service.forecast_direction(data_type=DataType.DAILY)

    assert predictions == 1 or predictions == 0
