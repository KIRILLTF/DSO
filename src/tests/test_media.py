from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_register_login_create_media():
    # Регистрация
    r = client.post(
        "/auth/register",
        json={"username": "test1", "password": "123", "email": "test1@example.com"},
    )
    assert r.status_code == 201

    # Логин
    r = client.post("/auth/login", data={"username": "test1", "password": "123"})
    token = r.json()["access_token"]

    # Создание media
    r = client.post(
        "/media/",
        json={"title": "Inception", "type": "movie", "year": 2010},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    assert r.json()["title"] == "Inception"
