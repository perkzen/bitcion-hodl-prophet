from src.api.services import forecast_service
from src.utils.data import DataType


def test_hourly_price_forecast():
    predictions = forecast_service.forecast_price(data_type=DataType.HOURLY)
    price = predictions["price"]

    assert price > 0
    assert price < 100_000


def test_daily_price_forecast():
    predictions = forecast_service.forecast_price(data_type=DataType.DAILY)
    price = predictions["price"]

    assert price > 0
    assert price < 100_000


def test_hourly_direction_forecast():
    prediction = forecast_service.forecast_direction(data_type=DataType.HOURLY)
    direction = prediction["direction"]
    assert direction == "up" or direction == "down"


def test_daily_direction_forecast():
    prediction = forecast_service.forecast_direction(data_type=DataType.DAILY)
    direction = prediction["direction"]
    assert direction == "up" or direction == "down"
