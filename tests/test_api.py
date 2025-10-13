from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    r = client.post("/api/v1/register", params={"username": "u", "password": "p"})
    assert r.status_code == 200
    r = client.post("/api/v1/login", params={"username": "u", "password": "p"})
    assert "access_token" in r.json()
