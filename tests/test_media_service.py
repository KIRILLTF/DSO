from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.database import get_db
from src.domain.models import Media, User
from src.domain.schemas import MediaUpdate
from src.services.media_service import MediaService


def test_media_service_update_permission_denied():
    """Тест обновления медиа без прав"""
    db = next(get_db())
    try:
        # Mock текущего пользователя (не владелец)
        current_user = User(id=2, username="other", password="hash", role="user")

        # Mock медиа принадлежащего другому пользователю
        media = Media(id=1, title="Test", user_id=1)

        with patch("src.services.media_service.repo_get", return_value=media):
            update_data = MediaUpdate(title="New Title")

            with pytest.raises(HTTPException) as exc_info:
                MediaService.update(db, 1, update_data, current_user)

            assert exc_info.value.status_code == 403
            assert "Not enough permissions" in str(exc_info.value.detail)
    finally:
        db.close()


def test_media_service_update_admin_success():
    """Тест обновления медиа админом"""
    db = next(get_db())
    try:
        # Mock админа
        admin_user = User(id=2, username="admin", password="hash", role="admin")

        # Mock медиа принадлежащего другому пользователю
        media = Media(id=1, title="Test", user_id=1)

        with patch("src.services.media_service.repo_get", return_value=media):
            with patch("src.services.media_service.repo_update") as mock_update:
                mock_update.return_value = Media(id=1, title="New Title", user_id=1)

                update_data = MediaUpdate(title="New Title")
                result = MediaService.update(db, 1, update_data, admin_user)

                assert result.title == "New Title"
    finally:
        db.close()


def test_media_service_delete_permission_denied():
    """Тест удаления медиа без прав"""
    db = next(get_db())
    try:
        # Mock текущего пользователя (не владелец)
        current_user = User(id=2, username="other", password="hash", role="user")

        # Mock медиа принадлежащего другому пользователю
        media = Media(id=1, title="Test", user_id=1)

        with patch("src.services.media_service.repo_get", return_value=media):
            with pytest.raises(HTTPException) as exc_info:
                MediaService.delete(db, 1, current_user)

            assert exc_info.value.status_code == 403
    finally:
        db.close()


def test_media_service_delete_admin_success():
    """Тест удаления медиа админом"""
    db = next(get_db())
    try:
        # Mock админа
        admin_user = User(id=2, username="admin", password="hash", role="admin")

        # Mock медиа принадлежащего другому пользователю
        media = Media(id=1, title="Test", user_id=1)

        with patch("src.services.media_service.repo_get", return_value=media):
            with patch("src.services.media_service.repo_delete") as mock_delete:
                MediaService.delete(db, 1, admin_user)

                # Проверяем что delete был вызван
                mock_delete.assert_called_once()
    finally:
        db.close()
