from src.adapters import review_repository
from src.domain.models import Review
from src.domain.schemas import ReviewCreate


def list_reviews(limit=100, offset=0):
    return review_repository.get_all_reviews(limit=limit, offset=offset)


def add_review(data: ReviewCreate, owner_id: int):
    review = Review(**data.dict(), owner_id=owner_id)
    return review_repository.create_review(review)
