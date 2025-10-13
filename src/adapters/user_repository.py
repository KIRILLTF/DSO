from typing import Optional

from src.database import SessionLocal
from src.domain.models import User


class UserRepository:
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        return user

    def create_user(self, user: User) -> User:
        db = SessionLocal()
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user
