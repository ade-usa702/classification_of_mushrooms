import requests
from data import data

response = requests.post(
    "http://localhost:8000/predict/predict_batch",
    json=data
)
print(response.json())
