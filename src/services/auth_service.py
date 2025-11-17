# src/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.database import get_db
from src.domain.models import User
from src.domain.schemas import Token, UserCreate, UserResponse

# Выносим SECRET_KEY в environment variables для продакшн
SECRET_KEY = "your_secret_key"  # В продакшн заменить на os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(self, user: UserCreate) -> UserResponse:
        existing_user = (
            self.db.query(User).filter(User.username == user.username).first()
        )
        if existing_user:
            raise ValueError("Username already exists")

        new_user = User(
            username=user.username,
            password=self.get_password_hash(user.password),
            email=user.email,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return UserResponse(
            id=new_user.id, username=new_user.username, email=new_user.email
        )

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def login_user(self, username: str, password: str) -> Token:
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.create_access_token(data={"sub": str(user.id)})
        token_type = "bearer"
        return Token(access_token=access_token, token_type=token_type)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user
