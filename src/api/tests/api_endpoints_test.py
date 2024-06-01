from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_hourly_price_prediction_endpoint():
    response = client.get("/predict/price/hourly")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] > 0
    assert response.json()["prediction"] < 100_000


def test_daily_price_prediction_endpoint():
    response = client.get("/predict/price/daily")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] > 0
    assert response.json()["prediction"] < 100_000


def test_hourly_direction_prediction_endpoint():
    response = client.get("/predict/direction/hourly")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] == "up" or response.json()["prediction"] == "down"


def test_daily_direction_prediction_endpoint():
    response = client.get("/predict/direction/daily")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] == "up" or response.json()["prediction"] == "down"


def test_price_data_endpoint():
    response = client.get("/price/hourly")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



