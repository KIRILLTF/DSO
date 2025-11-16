from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.auth import get_current_user  # <- функция для проверки токена
from src.database import get_db
from src.domain.models import User
from src.domain.schemas import MediaCreate, MediaRead, MediaUpdate
from src.services.media_service import MediaService

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/", response_model=MediaRead, status_code=201)
def create_media(
    media: MediaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MediaService.create(db, media, current_user.id)


@router.get("/{media_id}", response_model=MediaRead)
def read_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MediaService.get(db, media_id)


@router.patch("/{media_id}", response_model=MediaRead)
def update_media(
    media_id: int,
    media: MediaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return MediaService.update(db, media_id, media, current_user)


@router.delete("/{media_id}", status_code=204)
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    MediaService.delete(db, media_id, current_user)
    return {"detail": "Media deleted"}
