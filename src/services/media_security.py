# src/services/media_security.py
import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile


class MediaSecurity:
    """Сервис для безопасной работы с медиа-файлами"""

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    MAX_FILE_SIZE_MB = 5
    ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/gif"}

    # Magic bytes для проверки типов файлов
    MAGIC_SIGNATURES = {
        b"\xff\xd8\xff": "image/jpeg",  # JPEG
        b"\x89PNG\r\n\x1a\n": "image/png",  # PNG
        b"GIF87a": "image/gif",  # GIF87a
        b"GIF89a": "image/gif",  # GIF89a
    }

    @classmethod
    def sniff_content_type(cls, data: bytes) -> str:
        """Определяем MIME-type по magic bytes"""
        for signature, mime_type in cls.MAGIC_SIGNATURES.items():
            if data.startswith(signature):
                return mime_type
        return None

    @classmethod
    def validate_file(cls, file: UploadFile) -> bytes:
        """Проверяет загружаемый файл на размер, тип и содержание"""
        # Проверяем расширение
        extension = file.filename.split(".")[-1].lower() if file.filename else ""
        if extension not in cls.ALLOWED_EXTENSIONS:
            error_msg = (
                f"Extension '{extension}' not allowed. "
                f"Allowed: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
            raise HTTPException(status_code=400, detail=error_msg)

        # Читаем и проверяем размер файла
        content = file.file.read()
        file_size = len(content)

        if file_size > cls.MAX_FILE_SIZE_MB * 1024 * 1024:
            size_mb = file_size / (1024 * 1024)
            error_msg = (
                f"File size {size_mb:.2f} MB exceeds "
                f"limit of {cls.MAX_FILE_SIZE_MB} MB"
            )
            raise HTTPException(status_code=400, detail=error_msg)

        # Проверяем magic bytes
        detected_type = cls.sniff_content_type(content)
        if not detected_type or detected_type not in cls.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail="File type doesn't match content or is not allowed",
            )

        # Проверяем соответствие заявленного типа и реального
        if file.content_type and file.content_type != detected_type:
            error_msg = (
                f"Declared content type '{file.content_type}' "
                f"doesn't match actual '{detected_type}'"
            )
            raise HTTPException(status_code=400, detail=error_msg)

        # Возвращаем указатель в начало
        file.file.seek(0)
        return content

    @staticmethod
    def secure_filename(filename: str) -> str:
        """Безопасное имя файла с UUID"""
        # Очищаем оригинальное имя
        original_name = os.path.basename(filename)
        name, ext = os.path.splitext(original_name)
        ext = ext.lower() if ext else ""

        # Генерируем безопасное имя
        safe_name = f"{uuid.uuid4()}{ext}"
        return safe_name

    @staticmethod
    def secure_save(file_content: bytes, upload_dir: Path, filename: str) -> Path:
        """Безопасное сохранение файла с проверкой пути"""
        upload_dir = upload_dir.resolve()
        file_path = (upload_dir / filename).resolve()

        # Защита от path traversal
        if not str(file_path).startswith(str(upload_dir)):
            raise ValueError("Path traversal attempt detected")

        # Проверяем симлинки
        if any(part.is_symlink() for part in file_path.parents):
            raise ValueError("Symlinks in path are not allowed")

        # Создаем директорию если не существует
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Сохраняем файл
        file_path.write_bytes(file_content)
        return file_path