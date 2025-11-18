import requests
import os

url = "http://localhost:8000/fit/"

# Открытие файла в бинарном режиме
filename = os.path.abspath("data/train_mushrooms.zip")
with open(filename, "rb") as f:
    files = {"filename": f}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())