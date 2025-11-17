from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_auth_api_simple():
    """Простой тест auth API"""

    import bcrypt

    from src.app.api.auth import create_access_token, verify_password

    # verify_password
    password = "test123"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False

    # create_access_token
    token = create_access_token({"sub": "1"})
    assert token is not None
    assert isinstance(token, str)


def test_media_repository_complete():
    """Полный тест media repository"""
    from src.adapters.media_repository import (
        create_media,
        delete_media,
        get_media_by_id,
        update_media,
    )
    from src.database import get_db
    from src.domain.schemas import MediaCreate, MediaUpdate

    db = next(get_db())
    try:
        # Создаем медиа
        media_data = MediaCreate(title="Repo Test", type="image")
        media = create_media(db, media_data, user_id=1)
        assert media.title == "Repo Test"

        # Получаем медиа
        media = get_media_by_id(db, media.id)
        assert media is not None

        # Обновляем медиа
        update_data = MediaUpdate(title="Updated Repo Test")
        updated_media = update_media(db, media, update_data)
        assert updated_media.title == "Updated Repo Test"

        # Удаляем медиа
        delete_media(db, media)

    finally:
        db.rollback()
        db.close()


def test_user_repository_complete():
    """Полный тест user repository"""
    from src.adapters.user_repository import UserRepository
    from src.database import get_db
    from src.domain.models import User

    repo = UserRepository()
    db = next(get_db())
    try:
        # Создаем пользователя
        import bcrypt

        hashed_password = bcrypt.hashpw(b"testpass", bcrypt.gensalt()).decode()
        user = User(
            username="repo_user", password=hashed_password, email="repo@test.com"
        )

        created_user = repo.create_user(user)
        assert created_user is not None
        assert created_user.username == "repo_user"

        # Ищем по ID
        found_user = repo.get_user_by_id(created_user.id)
        assert found_user is not None

        # Ищем по username
        found_user = repo.get_user_by_username("repo_user")
        assert found_user is not None

    finally:
        # Очищаем
        db.query(User).filter(User.username == "repo_user").delete()
        db.commit()
        db.close()


def test_media_security_complete():
    """Полный тест media security"""

    from src.services.media_security import MediaSecurity

    # Тестируем secure_filename
    safe_name = MediaSecurity.secure_filename("../../../etc/passwd.jpg")
    assert safe_name.endswith(".jpg")
    assert not safe_name.startswith("..")

    # Тестируем sniff_content_type
    png_data = b"\x89PNG\r\n\x1a\n" + b"x" * 100
    mime_type = MediaSecurity.sniff_content_type(png_data)
    assert mime_type == "image/png"


def test_auth_service_basic():
    """Базовый тест auth service"""

    from src.database import get_db
    from src.domain.schemas import Token
    from src.services.auth_service import AuthService

    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Тестируем create_access_token
        token = auth_service.create_access_token({"sub": "1"})
        assert token is not None

        # Тестируем login_user с моками
        with patch.object(auth_service, "authenticate_user") as mock_auth:
            mock_user = Mock(id=1, username="test")
            mock_auth.return_value = mock_user

            with patch.object(
                auth_service, "create_access_token", return_value="test_token"
            ):
                token = auth_service.login_user("test", "password")
                assert isinstance(token, Token)
                assert token.access_token == "test_token"

        # Тестируем базовые методы
        hash_result = auth_service.get_password_hash("password123")
        assert hash_result is not None

        result = auth_service.verify_password("wrong", hash_result)
        assert result is False

    finally:
        db.close()
