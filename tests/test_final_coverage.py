from unittest.mock import Mock, patch

import pytest

from src.database import get_db
from src.services.auth_service import AuthService


def test_auth_service_remaining_methods():
    """Тест оставшихся методов AuthService"""
    db = next(get_db())
    try:
        auth_service = AuthService(db)

        # Mock для оставшихся строк в auth_service
        with patch.object(db, "query") as mock_query:
            mock_filter = Mock()
            mock_first = Mock(return_value=None)
            mock_filter.first = mock_first
            mock_query.return_value.filter.return_value = mock_filter

            # Mock создания пользователя
            with patch.object(auth_service, "get_password_hash", return_value="hash"):
                with patch.object(db, "add"), patch.object(db, "commit"):
                    with patch.object(db, "refresh") as mock_refresh:
                        # Mock refresh чтобы установить ID
                        def set_id(user):
                            user.id = 1

                        mock_refresh.side_effect = set_id

                        # Это покроет оставшиеся строки
                        from src.domain.schemas import UserCreate

                        user_data = UserCreate(
                            username="testuser",
                            password="password123",
                            email="test@example.com",
                        )

                        result = auth_service.register_user(user_data)
                        assert result.id == 1
    finally:
        db.close()


def test_media_service_remaining():
    """Тест оставшихся строк media_service"""
    from src.database import get_db
    from src.domain.models import Media, User
    from src.services.media_service import MediaService

    db = next(get_db())
    try:
        # Mock для строки 23 (get media)
        with patch("src.services.media_service.repo_get", return_value=None):
            with pytest.raises(Exception) as exc_info:
                MediaService.get(db, 999)
            assert "not found" in str(exc_info.value).lower()

        # Mock для строки 29 (update permissions)
        current_user = User(id=2, username="user", password="hash", role="user")
        media = Media(id=1, title="Test", user_id=1)  # Принадлежит user_id=1

        with patch("src.services.media_service.repo_get", return_value=media):
            from src.domain.schemas import MediaUpdate

            update_data = MediaUpdate(title="New Title")

            with pytest.raises(Exception) as exc_info:
                MediaService.update(db, 1, update_data, current_user)
            assert "permissions" in str(exc_info.value).lower()

        # Mock для строки 42 (delete permissions)
        with patch("src.services.media_service.repo_get", return_value=media):
            with pytest.raises(Exception) as exc_info:
                MediaService.delete(db, 1, current_user)
            assert "permissions" in str(exc_info.value).lower()

    finally:
        db.close()


def test_review_service_simple():
    """Простой тест для review_service"""
    from src.domain.schemas import ReviewCreate
    from src.services.review_service import add_review

    with patch(
        "src.services.review_service.review_repository.create_review"
    ) as mock_create:
        from src.domain.models import Review

        mock_review = Review(id=1, content="Test", rating=5, owner_id=1)
        mock_create.return_value = mock_review

        review_data = ReviewCreate(content="Test", rating=5)
        result = add_review(review_data, owner_id=1)

        assert result.id == 1
