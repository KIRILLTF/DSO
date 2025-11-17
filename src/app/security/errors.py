# src/app/security/errors.py (дополнение)
import re
from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _mask_pii(detail: str) -> str:
    """Маскирует PII в деталях ошибки"""
    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "password": r'("password"\s*:\s*)"[^"]*"',
        "token": r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
    }
    masked = detail
    for field, pattern in patterns.items():
        if field == "password":
            masked = re.sub(pattern, r'\1"***MASKED***"', masked, flags=re.IGNORECASE)
        else:
            masked = re.sub(pattern, f"[MASKED_{field.upper()}]", masked)
    return masked


def problem(status: int, title: str, detail: str, type_: str = "about:blank"):
    """Возвращает ошибку в формате RFC 7807 с correlation_id и PII masking"""
    cid = str(uuid4())
    safe_detail = _mask_pii(detail)  # Маскируем PII
    return JSONResponse(
        {
            "type": type_,
            "title": title,
            "status": status,
            "detail": safe_detail,
            "correlation_id": cid,
        },
        status_code=status,
        headers={"Content-Type": "application/problem+json"},
    )


# Остальные функции остаются без изменений...
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Обработчик HTTP исключений в формате RFC 7807"""
    return problem(
        status=exc.status_code,
        title=exc.detail,
        detail=exc.detail,
        type_=f"/errors/http/{exc.status_code}",
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации в формате RFC 7807"""
    errors = []
    for error in exc.errors():
        errors.append({"loc": error["loc"], "msg": error["msg"], "type": error["type"]})

    return problem(
        status=422,
        title="Validation Error",
        detail="One or more validation errors occurred",
        type_="/errors/validation",
    )
