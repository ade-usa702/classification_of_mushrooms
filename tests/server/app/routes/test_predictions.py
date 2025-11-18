from unittest.mock import patch
from urllib.parse import urlencode
from fastapi.testclient import TestClient
from main import app  
from test_data import test_data, incomplete_data

client = TestClient(app)


def test_predict():
    response = client.get("/predict/", params=test_data[0])
    assert response.status_code == 200
    json_data = response.json()
    assert "poisonous" in json_data
    assert isinstance(json_data["poisonous"], bool)


def test_predict_missing_field():    
    response = client.get("/predict/", params=incomplete_data)
    # Должен возвращать 422, так как Pydantic валидирует входные данные
    assert response.status_code == 422


def test_predict_proba():
    response = client.get("/predict/predict_proba/", params=test_data[0])
    assert response.status_code == 200
    json_data = response.json()
    assert "probability_of_poisonous" in json_data
    assert json_data["probability_of_poisonous"] > 0


def test_predict_proba_missing_field():    
    response = client.get("/predict/predict_proba/", params=incomplete_data)
    assert response.status_code == 422


def test_predict_batch():
    response = client.post("/predict/predict_batch/", json=test_data)
    assert response.status_code == 200
    json_data = response.json()
    for i in json_data:
        assert "poisonous" in i
        assert isinstance(i["poisonous"], bool)


def test_predict_batch_missing_field():    
    response = client.post("/predict/predict_batch/", json=incomplete_data)
    assert response.status_code == 422


def test_predict_proba_batch():
    base_url = "/predict/predict_proba_batch?"

    params = []
    for row in test_data:
        for k, val in row.items():
            params.append((k, val))

    # Кодируем параметры в URL
    query_string = urlencode(params)
    url = base_url + query_string
    response = client.get(url)

    assert response.status_code == 200
    json_data = response.json()
    for i in json_data:
        assert "probability_of_poisonous" in i
        assert i["probability_of_poisonous"] > 0


def test_status():
    response = client.get("/predict/status/")
    assert response.status_code == 200
    json_data = response.json()
    assert "model_trained_at" in json_data
    assert json_data["model_trained_at"] is not None


def test_status_fail():
    with patch("app.routes.predictions.artifact", {}):
        response = client.get("/status")
        assert response.status_code == 404