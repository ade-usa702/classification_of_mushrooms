import requests
from data import data

url = "http://localhost:8000/predict/"

# Отправка прогноза по каждому грибу
predictions = []
for row in data:
    resp = requests.get(url, params=row)
    print(resp.json(), ", code:", resp.status_code)
    if resp.status_code == 200:
        predictions.append(resp.json())
    else:
        predictions.append({"error": resp.text})

# Объединение результатов с исходными данными
results = data.copy()
for i in range(len(results)):
    results[i]["poisonous"] = predictions[i].get("poisonous")

print(results)