from fastapi import FastAPI

from src.app.api.routes_auth import router as auth_router
from src.app.api.routes_media import router as media_router
from src.database import init_db

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
