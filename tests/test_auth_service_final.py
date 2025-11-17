from unittest.mock import Mock, patch

from src.database import get_db
from src.domain.models import User
from src.domain.schemas import UserCreate
from src.services.auth_service import AuthService, get_auth_service


def test_auth_service_get_auth_service():
    """Тест dependency get_auth_service"""
    db = next(get_db())
    try:
        auth_service = get_auth_service(db)
        assert isinstance(auth_service, AuthService)
    finally:
        db.close()


def test_auth_service_register_user_success():
    """Тест успешной регистрации пользователя"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock что пользователя нет в базе
        with patch.object(db, "query") as mock_query:
            mock_filter = Mock()
            mock_first = Mock(return_value=None)  # Пользователь не существует
            mock_filter.first = mock_first
            mock_query.return_value.filter.return_value = mock_filter

            # Mock хеширования пароля
            with patch.object(
                auth_service, "get_password_hash", return_value="hashed_password"
            ):
                user_data = UserCreate(
                    username="newuser", password="password123", email="new@example.com"
                )

                # Создаем mock пользователя с ID
                mock_user = User(
                    id=1,
                    username="newuser",
                    password="hashed_password",
                    email="new@example.com",
                )

                # Mock всех операций с базой
                with patch.object(db, "add") as mock_add, patch.object(
                    db, "commit"
                ) as mock_commit, patch.object(db, "refresh") as mock_refresh:
                    # Настраиваем refresh чтобы установить атрибуты
                    def refresh_side_effect(user):
                        user.id = 1

                    mock_refresh.side_effect = refresh_side_effect

                    response = auth_service.register_user(user_data)

                    # Проверяем что методы были вызваны
                    mock_add.assert_called_once()
                    mock_commit.assert_called_once()
                    mock_refresh.assert_called_once()

                    assert response.id == 1
                    assert response.username == "newuser"
                    assert response.email == "new@example.com"
    finally:
        db.close()


def test_auth_service_verify_password_success():
    """Тест verify_password с правильным паролем"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock правильной проверки пароля
        with patch("src.services.auth_service.pwd_context.verify", return_value=True):
            result = auth_service.verify_password("plain", "hashed")
            assert result is True
    finally:
        db.close()


def test_auth_service_verify_password_failure():
    """Тест verify_password с неправильным паролем"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock неправильной проверки пароля
        with patch("src.services.auth_service.pwd_context.verify", return_value=False):
            result = auth_service.verify_password("wrong", "hashed")
            assert result is False
    finally:
        db.close()


def test_auth_service_get_password_hash():
    """Тест хеширования пароля"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        with patch(
            "src.services.auth_service.pwd_context.hash", return_value="hashed_password"
        ):
            result = auth_service.get_password_hash("password123")
            assert result == "hashed_password"
    finally:
        db.close()
