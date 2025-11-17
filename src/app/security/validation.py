import json
from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field


class Payment(BaseModel):
    model_config = dict(extra="forbid")
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3)
    occurred_at: datetime


def normalize(dt: datetime) -> datetime:
    """Переводим datetime в UTC без tzinfo"""
    return dt.astimezone(timezone.utc).replace(tzinfo=None)


def parse_payment(raw_json: str) -> Payment:
    """Парсим JSON без float, возвращаем валидированную модель"""
    data = json.loads(raw_json, parse_float=str)
    return Payment.model_validate(data)
