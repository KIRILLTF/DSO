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
