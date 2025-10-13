from src.database import SessionLocal
from src.domain.models import Review


def get_all_reviews(limit=100, offset=0):
    db = SessionLocal()
    reviews = db.query(Review).offset(offset).limit(limit).all()
    db.close()
    return reviews


def create_review(review: Review):
    db = SessionLocal()
    db.add(review)
    db.commit()
    db.refresh(review)
    db.close()
    return review
