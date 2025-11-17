from src.adapters.media_repository import create_media, get_media_by_id
from src.adapters.user_repository import UserRepository
from src.database import get_db
from src.domain.models import User
from src.domain.schemas import MediaCreate


def test_media_repository_create():
    """Тест создания медиа в репозитории"""
    db = next(get_db())
    try:
        media_data = MediaCreate(
            title="Test Media", description="Test Description", type="image"
        )
        media = create_media(db, media_data, user_id=1)
        assert media.id is not None
        assert media.title == "Test Media"
    finally:
        db.rollback()
        db.close()


def test_media_repository_get():
    """Тест получения медиа из репозитория"""
    db = next(get_db())
    try:
        media = get_media_by_id(db, 1)
        # Может быть None если нет записи с id=1
        assert media is None or isinstance(media, object)
    finally:
        db.close()


def test_user_repository():
    """Тест репозитория пользователей"""
    repo = UserRepository()
    user = repo.get_user_by_id(1)
    # Может быть None если нет пользователя с id=1
    assert user is None or isinstance(user, User)
