from typing import Optional

from pydantic import BaseModel


# -------------------
# Пользователь
# -------------------
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    email: Optional[str] = None


class UserResponse(UserBase):
    id: int
    email: Optional[str] = None

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# -------------------
# Медиаресурс
# -------------------
class MediaBase(BaseModel):
    title: str
    description: Optional[str] = None


class MediaCreate(MediaBase):
    type: str


class MediaUpdate(MediaBase):
    type: Optional[str] = None


class MediaRead(MediaBase):
    id: int
    type: str
    user_id: int  # исправлено с owner_id на user_id

    model_config = {"from_attributes": True}
