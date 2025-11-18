import requests

url = "http://localhost:8000/predict/status/"

resp = requests.get(url)
print(resp.json())