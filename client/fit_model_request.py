import requests
import os
from server.utils.logger import log

url = "http://localhost:8000/fit/"

# Открытие файла в бинарном режиме
filename = os.path.abspath("data/train_mushrooms.zip")
with open(filename, "rb") as f:
    files = {"filename": f}
    response = requests.post(url, files=files)

log.info(f"Status code: {response.status_code}")
log.info(f"Response: {response.json()}")