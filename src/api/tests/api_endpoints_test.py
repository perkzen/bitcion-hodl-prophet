from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_hourly_price_prediction_endpoint():
    response = client.get("/predict/price/hourly")
    price = response.json()["price"]

    assert response.status_code == 200
    assert "price" in response.json()
    assert "date" in response.json()
    assert price > 0
    assert price < 100_000


def test_daily_price_prediction_endpoint():
    response = client.get("/predict/price/daily")
    price = response.json()["price"]

    assert response.status_code == 200
    assert "price" in response.json()
    assert "date" in response.json()
    assert price > 0
    assert price < 100_000


def test_hourly_direction_prediction_endpoint():
    response = client.get("/predict/direction/hourly")
    direction = response.json()["direction"]

    assert response.status_code == 200
    assert "direction" in response.json()
    assert "date" in response.json()
    assert direction == "up" or direction == "down"


def test_daily_direction_prediction_endpoint():
    response = client.get("/predict/direction/daily")
    direction = response.json()["direction"]

    assert response.status_code == 200
    assert "direction" in response.json()
    assert "date" in response.json()
    assert direction == "up" or direction == "down"


def test_price_data_endpoint():
    response = client.get("/price/hourly")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
