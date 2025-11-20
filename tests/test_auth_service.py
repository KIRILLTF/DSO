from src.database import get_db
from src.services.auth_service import AuthService


def test_auth_service_initialization():
    """Тест инициализации AuthService"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)
        assert auth_service is not None
        assert hasattr(auth_service, "db")
    finally:
        db.close()


def test_password_hashing():
    """Тест хеширования паролей"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)
        password = "testpassword123"
        hashed = auth_service.get_password_hash(password)
        assert hashed != password
        assert auth_service.verify_password(password, hashed)
    finally:
        db.close()
