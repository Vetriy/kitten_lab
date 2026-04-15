import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "kitten-api"


def test_create_kitten():
    data = {"name": "Мурзик", "age": 6, "color": "рыжий", "breed": "дворовой"}
    response = client.post("/kittens/", params=data)
    assert response.status_code == 200
    assert response.json()["name"] == "Мурзик"


def test_get_kittens():
    response = client.get("/kittens/")
    assert response.status_code == 200


def test_delete_kitten():
    data = {"name": "Барсик", "age": 2, "color": "черный", "breed": "британец"}
    create = client.post("/kittens/", params=data)
    kitten_id = create.json()["id"]

    delete = client.delete(f"/kittens/{kitten_id}")
    assert delete.status_code == 200
