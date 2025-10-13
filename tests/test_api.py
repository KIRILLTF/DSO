from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_register_and_login():
    r = client.post("/auth/register", json={"username": "u", "password": "p", "email": "test@example.com"})
    assert r.status_code == 201
    r = client.post("/auth/login", data={"username": "u", "password": "p"})
    assert "access_token" in r.json()
