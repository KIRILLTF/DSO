from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from src.database import get_db
from src.domain.models import User
from src.domain.schemas import Token, UserCreate
from src.services.auth_service import AuthService


def test_auth_service_register_existing_user():
    """Тест регистрации существующего пользователя"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Создаем mock пользователя который уже существует
        with patch.object(db, "query") as mock_query:
            mock_filter = Mock()
            mock_first = Mock(
                return_value=User(id=1, username="existing", password="hash")
            )
            mock_filter.first = mock_first
            mock_query.return_value.filter.return_value = mock_filter

            with pytest.raises(ValueError, match="Username already exists"):
                auth_service.register_user(
                    UserCreate(
                        username="existing",
                        password="password123",
                        email="test@example.com",
                    )
                )
    finally:
        db.close()


def test_auth_service_authenticate_user_success():
    """Тест успешной аутентификации"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock успешной проверки пароля
        with patch.object(auth_service, "verify_password", return_value=True):
            with patch.object(db, "query") as mock_query:
                mock_filter = Mock()
                mock_first = Mock(
                    return_value=User(id=1, username="test", password="hash")
                )
                mock_filter.first = mock_first
                mock_query.return_value.filter.return_value = mock_filter

                user = auth_service.authenticate_user("test", "password123")
                assert user is not None
                assert user.username == "test"
    finally:
        db.close()


def test_auth_service_authenticate_user_failure():
    """Тест неудачной аутентификации"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock пользователя не найден
        with patch.object(db, "query") as mock_query:
            mock_filter = Mock()
            mock_first = Mock(return_value=None)
            mock_filter.first = mock_first
            mock_query.return_value.filter.return_value = mock_filter

            user = auth_service.authenticate_user("nonexistent", "password")
            assert user is None

        # Mock неверного пароля
        with patch.object(db, "query") as mock_query:
            mock_filter = Mock()
            mock_first = Mock(return_value=User(id=1, username="test", password="hash"))
            mock_filter.first = mock_first
            mock_query.return_value.filter.return_value = mock_filter

            with patch.object(auth_service, "verify_password", return_value=False):
                user = auth_service.authenticate_user("test", "wrongpassword")
                assert user is None
    finally:
        db.close()


def test_auth_service_login_user():
    """Тест логина пользователя"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock успешной аутентификации
        with patch.object(auth_service, "authenticate_user") as mock_auth:
            mock_auth.return_value = User(id=1, username="test", password="hash")
            with patch.object(
                auth_service, "create_access_token", return_value="test_token"
            ):
                token = auth_service.login_user("test", "password123")
                assert isinstance(token, Token)
                assert token.access_token == "test_token"
                assert token.token_type == "bearer"

        # Mock неудачной аутентификации
        with patch.object(auth_service, "authenticate_user", return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                auth_service.login_user("test", "wrongpassword")
            assert exc_info.value.status_code == 401
    finally:
        db.close()


def test_auth_service_create_access_token():
    """Тест создания access token"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        token = auth_service.create_access_token({"sub": "1"})
        assert token is not None
        assert isinstance(token, str)

        # С custom expires_delta
        from datetime import timedelta

        token = auth_service.create_access_token(
            {"sub": "1"}, expires_delta=timedelta(minutes=30)
        )
        assert token is not None
    finally:
        db.close()
