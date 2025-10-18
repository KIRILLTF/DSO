# src/services/media_security.py

import os

from fastapi import HTTPException, UploadFile


class MediaSecurity:
    """
    Сервис для безопасной работы с медиа-файлами:
    - Проверка размера
    - Проверка расширения
    - Ограничение доступа
    """

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    MAX_FILE_SIZE_MB = 5
    ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/gif"}

    def is_allowed(self, file_name: str, content_type: str, size: int) -> bool:
        ext = file_name.split(".")[-1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return False
        if content_type not in self.ALLOWED_CONTENT_TYPES:
            return False
        if size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
            return False
        return True

    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """
        Проверяет загружаемый файл на размер и тип
        """
        extension = file.filename.split(".")[-1].lower()
        if extension not in MediaSecurity.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail=f"Extension '{extension}' not allowed"
            )

        # Проверяем размер
        file.file.seek(0, os.SEEK_END)
        size_mb = file.file.tell() / (1024 * 1024)
        file.file.seek(0)
        if size_mb > MediaSecurity.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File size {size_mb:.2f} MB exceeds limit of "
                f"{MediaSecurity.MAX_FILE_SIZE_MB} MB",
            )

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Простая очистка имени файла
        """
        return os.path.basename(filename)
