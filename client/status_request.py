import requests
from server.utils.logger import log

url = "http://localhost:8000/predict/status/"

resp = requests.get(url)
log.info(f"Response: {resp.json()}")