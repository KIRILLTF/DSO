from unittest.mock import Mock, patch

import pytest

from src.database import get_db
from src.services.auth_service import AuthService


def test_media_service_missing_lines():
    """Тест оставшихся строк в media_service"""
    from unittest.mock import Mock, patch

    from src.services.media_service import MediaService

    db = next(get_db())
    try:
        # Строка 29 - update permission denied
        user = Mock(id=2, role="user")
        media_mock = Mock()
        media_mock.user_id = 1  # Принадлежит другому пользователю

        with patch("src.services.media_service.repo_get", return_value=media_mock):
            from src.domain.schemas import MediaUpdate

            with pytest.raises(Exception) as exc:
                MediaService.update(db, 1, MediaUpdate(title="Test"), user)
            assert "permissions" in str(exc.value).lower()

        # Строка 42 - delete permission denied
        with patch("src.services.media_service.repo_get", return_value=media_mock):
            with pytest.raises(Exception) as exc:
                MediaService.delete(db, 1, user)
            assert "permissions" in str(exc.value).lower()

    finally:
        db.close()


def test_auth_api_missing_lines():
    """Тест оставшихся строк в auth API"""
    from unittest.mock import Mock, patch

    from fastapi import HTTPException
    from jose import JWTError

    from src.app.api.auth import get_current_user

    db = next(get_db())
    try:
        # Создаем mock credentials
        mock_credentials = Mock()
        mock_credentials.credentials = "test_token"

        # Тестируем строки 44-61 (обработка ошибок)

        # JWTError
        with patch("src.app.api.auth.jwt.decode", side_effect=JWTError("Invalid")):
            with pytest.raises(HTTPException) as exc_info:
                import asyncio

                asyncio.run(get_current_user(mock_credentials, db))
            assert exc_info.value.status_code == 401

        # No sub in token
        with patch("src.app.api.auth.jwt.decode") as mock_decode:
            mock_decode.return_value = {"no_sub": "value"}

            with pytest.raises(HTTPException) as exc_info:
                import asyncio

                asyncio.run(get_current_user(mock_credentials, db))
            assert exc_info.value.status_code == 401

    finally:
        db.close()


def test_auth_service_error_cases():
    """Тест случаев ошибок в auth service"""
    from src.domain.schemas import UserCreate

    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Тестируем регистрацию существующего пользователя
        with patch.object(db, "query") as mock_query:
            mock_filter = Mock()
            mock_filter.first.return_value = Mock()  # Пользователь существует

            mock_query.filter.return_value = mock_filter

            with pytest.raises(ValueError) as exc:
                user_data = UserCreate(
                    username="existing", password="pass", email="test@test.com"
                )
                auth_service.register_user(user_data)
            assert "already exists" in str(exc.value)

    finally:
        db.close()
