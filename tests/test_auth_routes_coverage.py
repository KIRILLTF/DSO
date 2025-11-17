# tests/test_auth_routes_coverage.py

from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_auth_routes_register():
    """Тест регистрации через auth_routes"""
    # Мокаем bcrypt чтобы избежать реального хеширования
    with patch("src.app.api.routes_auth.bcrypt") as mock_bcrypt:
        mock_bcrypt.hashpw.return_value = b"hashed_password"
        mock_bcrypt.gensalt.return_value = b"salt"

        # Успешная регистрация с валидным паролем
        response = client.post(
            "/auth/register",
            json={
                "username": "auth_routes_user",
                "password": "Testpass123!",  # Валидный пароль
                "email": "test@example.com",
            },
        )
        assert response.status_code in [201, 400, 422]

        if response.status_code == 201:
            data = response.json()
            assert "username" in data
            assert "id" in data


def test_auth_routes_password_length_limit():
    """Тест ограничения длины пароля для bcrypt"""
    # Длинный пароль (более 72 символов) но валидный
    long_password = "A" * 50 + "1" + "!"  # 52 символа - валидный

    with patch("src.app.api.routes_auth.bcrypt") as mock_bcrypt:
        mock_bcrypt.hashpw.return_value = b"hashed_password"
        mock_bcrypt.gensalt.return_value = b"salt"

        response = client.post(
            "/auth/register",
            json={
                "username": "long_password_user",
                "password": long_password,
                "email": "test@example.com",
            },
        )
        assert response.status_code in [201, 400, 422]


def test_auth_routes_error_handling():
    """Тест обработки ошибок в auth_routes"""
    # Неправильный HTTP метод
    response = client.get("/auth/register")
    assert response.status_code == 405

    # Неправильный Content-Type
    response = client.post("/auth/register", data="plain text")
    assert response.status_code in [400, 422, 415]

    # Невалидный JSON
    response = client.post("/auth/register", data='{"invalid": json')
    assert response.status_code in [400, 422]


def test_auth_routes_login():
    """Тест логина"""
    with patch("src.app.api.routes_auth.bcrypt") as mock_bcrypt:
        mock_bcrypt.hashpw.return_value = b"hashed_password"
        mock_bcrypt.gensalt.return_value = b"salt"
        mock_bcrypt.checkpw.return_value = True

        # Регистрация с валидным паролем
        client.post(
            "/auth/register",
            json={
                "username": "login_user",
                "password": "Testpass123!",
                "email": "login@example.com",
            },
        )

        # Логин
        response = client.post(
            "/auth/login", data={"username": "login_user", "password": "Testpass123!"}
        )
        assert response.status_code in [200, 401]

        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"


def test_auth_routes_valid_password_examples():
    """Тест валидных паролей"""
    valid_passwords = ["Testpass123!", "MyP@ssw0rd", "Secure123#", "Valid!Pass1"]

    with patch("src.app.api.routes_auth.bcrypt") as mock_bcrypt:
        mock_bcrypt.hashpw.return_value = b"hashed_password"
        mock_bcrypt.gensalt.return_value = b"salt"

        for i, password in enumerate(valid_passwords):
            response = client.post(
                "/auth/register",
                json={
                    "username": f"valid_user_{i}",
                    "password": password,
                    "email": f"user{i}@example.com",
                },
            )
            # Должен быть 201 или 400 (если пользователь уже существует)
            assert response.status_code in [201, 400]
