import pytest

from src.database import get_db
from src.domain.schemas import MediaCreate
from src.services.media_service import MediaService


def test_media_service_create():
    """Тест создания медиа через MediaService"""
    db = next(get_db())
    try:
        media_data = MediaCreate(
            title="Test Media", description="Test Description", type="image"
        )
        media = MediaService.create(db, media_data, user_id=1)
        assert media.id is not None
        assert media.title == "Test Media"
    finally:
        db.rollback()
        db.close()


def test_media_service_get_not_found():
    """Тест получения несуществующего медиа"""
    db = next(get_db())
    try:
        # Должен вернуть 404 для несуществующего ID
        with pytest.raises(Exception) as exc_info:
            MediaService.get(db, 99999)
        assert "not found" in str(exc_info.value).lower()
    finally:
        db.close()
