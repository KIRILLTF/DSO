import sys
from io import BytesIO
from pathlib import Path

import pytest
from fastapi import UploadFile

from src.services.media_security import MediaSecurity


def test_media_security_magic_bytes_png():
    """Тест проверки PNG файла по magic bytes"""
    png_data = b"\x89PNG\r\n\x1a\n" + b"x" * 100  # Valid PNG header
    file = UploadFile(filename="test.png", file=BytesIO(png_data))

    content = MediaSecurity.validate_file(file)
    assert content == png_data


def test_media_security_magic_bytes_jpeg():
    """Тест проверки JPEG файла по magic bytes"""
    jpeg_data = b"\xff\xd8\xff" + b"x" * 100  # Valid JPEG header
    file = UploadFile(filename="test.jpg", file=BytesIO(jpeg_data))

    content = MediaSecurity.validate_file(file)
    assert content == jpeg_data


def test_media_security_fake_extension():
    """Тест на подмену расширения"""
    # PNG content with .exe extension
    png_data = b"\x89PNG\r\n\x1a\n" + b"x" * 100
    file = UploadFile(filename="malicious.exe", file=BytesIO(png_data))

    with pytest.raises(Exception) as exc_info:
        MediaSecurity.validate_file(file)
    assert "not allowed" in str(exc_info.value)


def test_media_security_invalid_magic_bytes():
    """Тест на невалидные magic bytes"""
    invalid_data = b"INVALID_CONTENT" * 1000
    file = UploadFile(filename="test.jpg", file=BytesIO(invalid_data))

    with pytest.raises(Exception) as exc_info:
        MediaSecurity.validate_file(file)
    assert "File type doesn't match" in str(exc_info.value)


def test_secure_filename():
    """Тест генерации безопасного имени файла"""
    dangerous_name = "../../../etc/passwd"
    safe_name = MediaSecurity.secure_filename(dangerous_name)

    # Проверяем что имя безопасное (убрали проверку на расширение)
    assert not safe_name.startswith("..")  # убирает path traversal
    assert len(safe_name) == 36  # UUID без расширения (файл без расширения)


def test_secure_save_path_traversal():
    """Тест защиты от path traversal при сохранении"""
    upload_dir = Path("/safe/upload/dir")
    malicious_path = "../../etc/passwd"

    with pytest.raises(ValueError, match="Path traversal"):
        MediaSecurity.secure_save(b"content", upload_dir, malicious_path)


def test_file_size_limit():
    """Тест ограничения размера файла"""
    large_data = b"x" * (6 * 1024 * 1024)  # 6MB > 5MB limit
    file = UploadFile(filename="large.jpg", file=BytesIO(large_data))

    with pytest.raises(Exception) as exc_info:
        MediaSecurity.validate_file(file)
    assert "exceeds limit" in str(exc_info.value)
