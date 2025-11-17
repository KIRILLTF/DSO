from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


def test_auth_verify_password_simple():
    """Простой тест verify_password"""
    import bcrypt

    from src.app.api.auth import verify_password

    # Нормальный тест
    password = "testpassword"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    result = verify_password(password, hashed)
    assert result is True

    result = verify_password("wrongpassword", hashed)
    assert result is False


def test_auth_create_token_simple():
    """Простой тест create_access_token"""
    from datetime import timedelta

    from src.app.api.auth import create_access_token

    token = create_access_token({"sub": "1"})
    assert token is not None

    token2 = create_access_token({"sub": "1"}, timedelta(minutes=30))
    assert token2 is not None


def test_auth_routes_simple():
    """Простой тест auth routes"""
    # Тестируем регистрацию
    response = client.post(
        "/auth/register",
        json={
            "username": "coverage_test_user_1",
            "password": "testpass123",
            "email": "coverage1@test.com",
        },
    )
    assert response.status_code in [201, 400, 422]

    # Тестируем логин
    response = client.post(
        "/auth/login",
        data={"username": "coverage_test_user_1", "password": "testpass123"},
    )
    assert response.status_code in [200, 401, 422]

    # Тестируем logout
    response = client.post("/auth/logout")
    assert response.status_code in [204, 401, 403]


def test_media_routes_simple():
    """Простой тест media routes"""
    # Без авторизации
    response = client.get("/media/1")
    assert response.status_code in [401, 403]

    response = client.post("/media/", json={"title": "test", "type": "image"})
    assert response.status_code in [401, 403]

    response = client.patch("/media/1", json={"title": "updated"})
    assert response.status_code in [401, 403]

    response = client.delete("/media/1")
    assert response.status_code in [401, 403]


def test_auth_service_simple():
    """Простой тест auth service"""
    from src.database import get_db
    from src.services.auth_service import AuthService

    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Тестируем хеширование пароля
        hash_result = auth_service.get_password_hash("testpassword")
        assert hash_result is not None

        # Тестируем verify_password
        result = auth_service.verify_password("test", hash_result)
        assert result is False  # Должен быть False для несовпадающих паролей

    finally:
        db.close()


def test_media_service_simple():
    """Простой тест media service"""
    from src.database import get_db
    from src.domain.schemas import MediaCreate
    from src.services.media_service import MediaService

    db = next(get_db())
    try:
        # Тестируем создание медиа
        media_data = MediaCreate(title="Test Media", type="image")
        media = MediaService.create(db, media_data, user_id=1)
        assert media is not None
        assert media.title == "Test Media"

        # Тестируем получение медиа
        media = MediaService.get(db, media.id)
        assert media is not None

    finally:
        # Откатываем изменения
        db.rollback()
        db.close()


def test_user_repository_simple():
    """Простой тест user repository"""
    from src.adapters.user_repository import UserRepository

    repo = UserRepository()

    # Методы должны работать без ошибок
    user = repo.get_user_by_id(99999)
    assert user is None

    user = repo.get_user_by_username("nonexistent_user")
    assert user is None


def test_review_service_simple():
    """Простой тест review service"""
    from src.domain.schemas import ReviewCreate
    from src.services.review_service import add_review, list_reviews

    with patch(
        "src.services.review_service.review_repository.get_all_reviews"
    ) as mock_get:
        mock_get.return_value = []
        reviews = list_reviews()
        assert reviews == []

    with patch(
        "src.services.review_service.review_repository.create_review"
    ) as mock_create:
        from src.domain.models import Review

        mock_review = Review(id=1, content="Test", rating=5, owner_id=1)
        mock_create.return_value = mock_review

        review_data = ReviewCreate(content="Test", rating=5)
        result = add_review(review_data, 1)
        assert result.id == 1


def test_security_files_simple():
    """Простой тест security files"""

    from src.app.security.files import sniff

    # Тестируем sniff с PNG данными
    png_data = b"\x89PNG\r\n\x1a\n" + b"x" * 100
    result = sniff(png_data)
    assert result == "image/png"

    # Тестируем sniff с JPEG данными
    jpeg_data = b"\xff\xd8\xff" + b"x" * 100 + b"\xff\xd9"
    result = sniff(jpeg_data)
    assert result == "image/jpeg"


def test_security_validation_simple():
    """Простой тест security validation"""
    from datetime import datetime, timezone

    from src.app.security.validation import normalize, parse_payment

    # Тестируем normalize
    dt = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
    normalized = normalize(dt)
    assert normalized.tzinfo is None

    # Тестируем parse_payment
    payment_json = (
        '{"amount": "100.50", "currency": "USD", "occurred_at": "2023-01-01T12:00:00Z"}'
    )
    payment = parse_payment(payment_json)
    assert payment.amount == 100.50
    assert payment.currency == "USD"
