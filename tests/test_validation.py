from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.app.security.validation import normalize, parse_payment


def test_parse_payment_ok():
    raw = (
        '{"amount": "123.45", "currency": "USD", "occurred_at": "2025-01-01T12:00:00Z"}'
    )
    p = parse_payment(raw)
    assert p.amount == Decimal("123.45")
    assert p.currency == "USD"


def test_parse_payment_invalid_amount():
    raw = '{"amount": "-1.0", "currency": "USD", "occurred_at": "2025-01-01T12:00:00Z"}'
    with pytest.raises(ValidationError):
        parse_payment(raw)


def test_parse_payment_invalid_currency():
    raw = '{"amount": "10", "currency": "US", "occurred_at": "2025-01-01T12:00:00Z"}'
    with pytest.raises(ValidationError):
        parse_payment(raw)


def test_normalize_datetime():
    dt = datetime(2025, 1, 1, 12, 0, tzinfo=timezone.utc)
    norm = normalize(dt)
    assert norm.tzinfo is None
