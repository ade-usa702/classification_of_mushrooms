import requests
from data import data
from server.utils.logger import log

url = "http://localhost:8000/predict/predict_proba/"

# Отправка прогноза по каждому грибу
predictions = []
for row in data:
    resp = requests.get(url, params=row)
    log.info(f"Request: {resp.json()}, code: {resp.status_code}")
    if resp.status_code == 200:
        predictions.append(resp.json())
    else:
        predictions.append({"error": resp.text})

# Объединение результатов с исходными данными
results = data.copy()
for i in range(len(results)):
    results[i]["probability_of_poisonous"] = predictions[i].get("probability_of_poisonous")

log.info(f"Results: {results}")