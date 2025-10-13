from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.media_repository import create_media as repo_create
from src.adapters.media_repository import delete_media as repo_delete
from src.adapters.media_repository import get_media_by_id as repo_get
from src.adapters.media_repository import update_media as repo_update
from src.domain.schemas import MediaCreate, MediaUpdate


class MediaService:
    @staticmethod
    def create(db: Session, media_data: MediaCreate, user_id: int):
        return repo_create(db, media_data, user_id)

    @staticmethod
    def get(db: Session, media_id: int):
        media = repo_get(db, media_id)
        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
            )
        return media

    @staticmethod
    def update(db: Session, media_id: int, media_data: MediaUpdate, current_user):
        media = repo_get(db, media_id)
        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
            )
        if media.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return repo_update(db, media, media_data)

    @staticmethod
    def delete(db: Session, media_id: int, current_user):
        media = repo_get(db, media_id)
        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Media not found"
            )
        if media.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        repo_delete(db, media)
