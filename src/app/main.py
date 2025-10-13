from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.app.api.auth import get_current_user
from src.app.api.routes_auth import router as auth_router
from src.app.api.routes_media import router as media_router
from src.database import get_db, init_db
from src.domain.schemas import MediaCreate, MediaUpdate
from src.services.media_service import MediaService

app = FastAPI(title="My Project")

# Инициализация базы
init_db()

# Подключаем маршруты
app.include_router(auth_router, tags=["auth"])
app.include_router(media_router, tags=["media"])


# Пример middleware (можно оставлять для request logging, request_id и т.п.)
@app.middleware("http")
async def add_request_id(request, call_next):
    response = await call_next(request)
    return response


# Примеры эндпоинтов media с JWT-защитой
@app.post("/media/media/", tags=["media"])
def create_media_endpoint(
    media: MediaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return MediaService.create(db, media, current_user.id)


@app.put("/media/media/{media_id}", tags=["media"])
def update_media_endpoint(
    media_id: int,
    media: MediaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return MediaService.update(db, media_id, media, current_user)


@app.delete("/media/media/{media_id}", tags=["media"])
def delete_media_endpoint(
    media_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    MediaService.delete(db, media_id, current_user)
    return {"detail": "Media deleted"}


@app.get("/media/media/{media_id}", tags=["media"])
def get_media_endpoint(
    media_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return MediaService.get(db, media_id)
