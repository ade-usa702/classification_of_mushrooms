import pytest
import os
from main import app  
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
        "fname",
        [
            ("data/train_mushrooms.zip"),
            (""),
        ]
)
def test_fit_model(fname):
    if fname:
        filename = os.path.abspath(fname)
        with open(filename, "rb") as f:
            files = {"filename": f}
            response = client.post(url="http://127.0.0.1:8000/fit/", files=files)
        assert response.status_code == 200
        assert isinstance(response.json()["success"], bool)
        os.remove("mushrooms_model.pkl")
    else:
        response = client.post(
            url="http://127.0.0.1:8000/fit/",
            files={}
        )
        assert response.status_code == 422
