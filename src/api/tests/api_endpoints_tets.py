from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_hourly_prediction_endpoint():
    response = client.get("/prediction/hourly")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] > 0
    assert response.json()["prediction"] < 100_000


def test_daily_prediction_endpoint():
    response = client.get("/prediction/daily")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] > 0
    assert response.json()["prediction"] < 100_000
