from unittest.mock import Mock, patch

import pytest

from src.database import get_db
from src.services.media_service import MediaService


def test_media_service_error_cases():
    """Тест случаев ошибок в media service"""
    db = next(get_db())
    try:
        # Тестируем get с несуществующим ID
        with patch("src.services.media_service.repo_get", return_value=None):
            with pytest.raises(Exception) as exc:
                MediaService.get(db, 99999)
            assert "not found" in str(exc.value).lower()

        # Тестируем update без прав
        user = Mock(id=2, role="user")
        media_mock = Mock()
        media_mock.user_id = 1  # Принадлежит другому пользователю

        with patch("src.services.media_service.repo_get", return_value=media_mock):
            from src.domain.schemas import MediaUpdate

            with pytest.raises(Exception) as exc:
                MediaService.update(db, 1, MediaUpdate(title="Test"), user)
            assert "permissions" in str(exc.value).lower()

        # Тестируем delete без прав
        with patch("src.services.media_service.repo_get", return_value=media_mock):
            with pytest.raises(Exception) as exc:
                MediaService.delete(db, 1, user)
            assert "permissions" in str(exc.value).lower()

    finally:
        db.close()


def test_auth_service_error_cases():
    """Тест случаев ошибок в auth service"""
    from src.database import get_db
    from src.domain.schemas import UserCreate
    from src.services.auth_service import AuthService

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
