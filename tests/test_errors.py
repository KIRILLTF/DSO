from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


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
        extra_data={"errors": errors},
    )


def problem(
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    extra_data: dict = None,
):
    """Возвращает ошибку в формате RFC 7807 с correlation_id"""
    cid = str(uuid4())
    response_data = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "correlation_id": cid,
    }

    if extra_data:
        response_data.update(extra_data)

    return JSONResponse(
        response_data,
        status_code=status,
        headers={"Content-Type": "application/problem+json"},
    )
