from fastapi import APIRouter, Depends

from src.domain.schemas import ReviewCreate, ReviewResponse
from src.services import review_service


def get_current_user_id():
    return 1  # TODO: заменить на авторизацию JWT


router = APIRouter()


@router.get("/", response_model=list[ReviewResponse])
def get_reviews(limit: int = 100, offset: int = 0):
    return review_service.list_reviews(limit=limit, offset=offset)


@router.post("/", response_model=ReviewResponse)
def add_review(review: ReviewCreate, owner_id: int = Depends(get_current_user_id)):
    return review_service.add_review(review, owner_id)
