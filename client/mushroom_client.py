import json
import os
import requests
from typing import List
from urllib.parse import urlencode
from data import data_list
from server.utils.logger import log


class MushroomClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Инициализация клиента

        Args:
            base_url (str, optional): url для подключения.
                     Defaults to "http://localhost:8000".
        """        
        self.base_url = base_url

    def predict(self, data: dict) -> dict:
        """Определение(предсказывание) гриба: ядовитый или съедобный.

        Args:
            data (dict): данные для ввода

        Returns:
            dict: Ответ сервера
        """
        resp = requests.get(f"{self.base_url}/predict/", params=data)
        log.info(f"Request: {resp.json()}, code: {resp.status_code}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    
    def predict_proba(self, data: dict) -> dict:
        """Определение(предсказывание) вероятности ядовитости гриба.

        Args:
            data (dict): данные для ввода

        Returns:
            dict: Ответ сервера
        """
        resp = requests.get(f"{self.base_url}/predict/predict_proba/", params=data)
        log.info(f"Request: {resp.json()}, code: {resp.status_code}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": resp.text}
    
    def predict_batch(self, data: List[dict]) -> dict:
        """Определение(предсказывание) списка грибов: ядовитый или съедобный.

        Args:
            data (List[dict]): данные для ввода

        Returns:
            dict: Ответ сервера
        """        
        response = requests.post(
            f"{self.base_url}/predict/predict_batch/",
            json=data
        )
        log.info(f"Response: {response.json()}")
        return response.json()
    
    def predict_proba_batch(self, data: List[dict]) -> dict:
        """Определение(предсказывание) вероятности ядовитости списка грибов.

        Args:
            data (List[dict]): данные для ввода

        Returns:
            dict: Ответ сервера
        """        
        # Формирование параметров GET-запроса
        base_url = f"{self.base_url}/predict/predict_proba_batch?"
        params = []
        for row in data:
            for k, val in row.items():
                params.append((k, val))

        # Кодировка параметров в URL
        query_string = urlencode(params)
        url = base_url + query_string

        log.info(f"GET url: {url}")

        # Отправка GET-запроса
        response = requests.get(url)
        log.info(f"Response: {response.json()}")
        return response.json()
    
    def status(self) -> dict: 
        """Возвращает дату, когда модель была обучена.

        Returns:
            dict: Ответ сервера
        """        
        resp = requests.get(f"{self.base_url}/predict/status/")
        log.info(f"Response: {resp.json()}")
        return resp.json()
    
    def fit_model(self, file_name: str) -> dict:
        """Обучение модели на загруженном файле с данными.

        Args:
            file_name (str): Имя файла

        Returns:
            dict: Ответ сервера
        """        
        # Открытие файла в бинарном режиме
        filename = os.path.abspath(file_name)
        with open(filename, "rb") as f:
            files = {"filename": f}
            response = requests.post(f"{self.base_url}/fit/", files=files)

        log.info(f"Status code: {response.status_code}")
        log.info(f"Response: {response.json()}")
        return response.json()
    

def main():
    """Запуск клиента"""    
    client = MushroomClient()
    try:
        print("1. Предсказывание ядовитости гриба:")
        predict = client.predict(data_list[0])
        print(json.dumps(predict, indent=2))

        print("\n2. Предсказывание вероятости ядовитости гриба:")
        predict_proba = client.predict_proba(data_list[0])
        print(json.dumps(predict_proba, indent=2))

        print("\n3. Предсказывание ядовитости списка грибов:")
        batch = client.predict_batch(data_list)
        print(json.dumps(batch, indent=2))

        print("\n4. Предсказывание вероятости ядовитости списка грибов:")
        batch_proba = client.predict_proba_batch(data_list)
        print(json.dumps(batch_proba, indent=2))

        print("\n5. Дата обучения модели:")
        status = client.status()
        print(json.dumps(status, indent=2))

        print("\n6. Обучение модели:")
        fit = client.fit_model("data/train_mushrooms.zip")
        print(json.dumps(fit, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
        print("Убедитесь, что сервер запущен на http://localhost:8000")


if __name__ == "__main__":
    main()