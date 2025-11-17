from src.adapters.media_repository import create_media, delete_media, get_media_by_id, update_media
from src.database import get_db
from src.domain.schemas import MediaCreate, MediaUpdate


def test_media_repository_create_success():
    """Тест успешного создания медиа"""
    db = next(get_db())
    try:
        media_data = MediaCreate(
            title="Test Media", description="Test Description", type="image"
        )

        media = create_media(db, media_data, user_id=1)
        assert media.id is not None
        assert media.title == "Test Media"
        assert media.description == "Test Description"
        assert media.type == "image"
        assert media.user_id == 1

        # Проверяем что можно получить созданное медиа
        retrieved = get_media_by_id(db, media.id)
        assert retrieved is not None
        assert retrieved.title == "Test Media"
    finally:
        db.rollback()
        db.close()


def test_media_repository_update_success():
    """Тест успешного обновления медиа"""
    db = next(get_db())
    try:
        # Сначала создаем медиа
        media_data = MediaCreate(
            title="Original Title", description="Original Description", type="image"
        )
        media = create_media(db, media_data, user_id=1)

        # Обновляем
        update_data = MediaUpdate(
            title="Updated Title", description="Updated Description"
        )
        updated_media = update_media(db, media, update_data)

        assert updated_media.title == "Updated Title"
        assert updated_media.description == "Updated Description"
        assert updated_media.type == "image"  # Не менялся
    finally:
        db.rollback()
        db.close()


def test_media_repository_update_partial():
    """Тест частичного обновления медиа"""
    db = next(get_db())
    try:
        media_data = MediaCreate(
            title="Original Title", description="Original Description", type="image"
        )
        media = create_media(db, media_data, user_id=1)

        # Обновляем только title
        update_data = MediaUpdate(title="New Title")
        updated_media = update_media(db, media, update_data)

        assert updated_media.title == "New Title"
        assert updated_media.description == "Original Description"  # Не изменилось
    finally:
        db.rollback()
        db.close()


def test_media_repository_delete_success():
    """Тест успешного удаления медиа"""
    db = next(get_db())
    try:
        media_data = MediaCreate(
            title="To Delete", description="Will be deleted", type="image"
        )
        media = create_media(db, media_data, user_id=1)
        media_id = media.id

        # Удаляем
        delete_media(db, media)

        # Проверяем что медиа больше нет
        deleted_media = get_media_by_id(db, media_id)
        assert deleted_media is None
    finally:
        db.rollback()
        db.close()


def test_media_repository_get_nonexistent():
    """Тест получения несуществующего медиа"""
    db = next(get_db())
    try:
        media = get_media_by_id(db, 99999)
        assert media is None
    finally:
        db.close()
