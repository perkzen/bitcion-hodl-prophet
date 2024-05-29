import numpy as np
from src.api.services import ml_service
from src.utils.data import DataType


def test_hourly_forecast():
    predictions = ml_service.forecast(data_type=DataType.HOURLY)

    assert predictions > 0
    assert isinstance(predictions, np.float32)
    assert predictions < 100_000


def test_daily_forecast():
    predictions = ml_service.forecast(data_type=DataType.DAILY)

    assert predictions > 0
    assert isinstance(predictions, np.float32)
    assert predictions < 100_000
