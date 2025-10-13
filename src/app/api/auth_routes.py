# src/app/api/auth_routes.py

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

# Создаем роутер
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Максимальная длина пароля для bcrypt
MAX_BCRYPT_PASSWORD_LENGTH = 72


# Схема для регистрации пользователя
class UserCreate(BaseModel):
    username: str
    password: str


# Заглушка для БД (заменить на реальный код)
fake_db = {}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    if user.username in fake_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    # Ограничиваем длину пароля до 72 байт для bcrypt
    password_to_hash = user.password[:MAX_BCRYPT_PASSWORD_LENGTH]
    hashed_password = pwd_context.hash(password_to_hash)

    # Сохраняем пользователя в "БД" (заменить на реальный код сохранения)
    fake_db[user.username] = hashed_password

    return {"username": user.username, "hashed_password": hashed_password}
