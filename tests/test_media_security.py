import pytest

from src.services.media_security import MediaSecurity


@pytest.fixture
def media_security():
    """Создаёт объект MediaSecurity для тестов."""
    return MediaSecurity()


def test_allowed_file(media_security):
    file_name = "sample.png"
    content_type = "image/png"
    size = 1024
    assert media_security.is_allowed(file_name, content_type, size) is True


def test_disallowed_extension(media_security):
    file_name = "sample.exe"
    content_type = "application/octet-stream"
    size = 1024
    assert media_security.is_allowed(file_name, content_type, size) is False


def test_disallowed_size(media_security):
    file_name = "sample.png"
    content_type = "image/png"
    size = 10 * 1024 * 1024  # 10 MB
    assert media_security.is_allowed(file_name, content_type, size) is False


def test_disallowed_content_type(media_security):
    file_name = "sample.png"
    content_type = "application/pdf"
    size = 1024
    assert media_security.is_allowed(file_name, content_type, size) is False
