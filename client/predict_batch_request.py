import requests
from data import data
from server.utils.logger import log

response = requests.post(
    "http://localhost:8000/predict/predict_batch",
    json=data
)
log.info(f"Response: {response.json()}")