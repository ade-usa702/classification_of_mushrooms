import requests
from data import data
from urllib.parse import urlencode


base_url = "http://localhost:8000/predict/predict_proba_batch?"

# Формирование параметров GET-запроса
params = []
for row in data:
    for k, val in row.items():
        params.append((k, val))

# Кодировка параметров в URL
query_string = urlencode(params)
url = base_url + query_string

print("GET URL:", url)

# Отправка GET-запроса
response = requests.get(url)
print(response.json())
