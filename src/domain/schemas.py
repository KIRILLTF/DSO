from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    email: str | None = None


class UserResponse(UserBase):
    id: int
    email: str | None = None

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class MediaBase(BaseModel):
    title: str
    description: str | None = None


class MediaCreate(MediaBase):
    type: str


class MediaUpdate(MediaBase):
    type: str | None = None


class MediaRead(MediaBase):
    id: int
    type: str
    user_id: int

    model_config = {"from_attributes": True}


class ReviewBase(BaseModel):
    content: str
    rating: int
    media_id: int | None = None


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
