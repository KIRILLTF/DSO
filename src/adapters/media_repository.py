from sqlalchemy.orm import Session

from src.domain.models import Media
from src.domain.schemas import MediaCreate, MediaUpdate


def create_media(db: Session, media_data: MediaCreate, user_id: int) -> Media:
    db_media = Media(
        title=media_data.title,
        description=media_data.description,
        type=media_data.type,
        user_id=user_id,
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def get_media_by_id(db: Session, media_id: int) -> Media | None:
    return db.query(Media).filter(Media.id == media_id).first()


def update_media(db: Session, media: Media, media_data: MediaUpdate) -> Media:
    if media_data.title is not None:
        media.title = media_data.title
    if media_data.description is not None:
        media.description = media_data.description
    if media_data.type is not None:
        media.type = media_data.type
    db.commit()
    db.refresh(media)
    return media


def delete_media(db: Session, media: Media):
    db.delete(media)
    db.commit()
