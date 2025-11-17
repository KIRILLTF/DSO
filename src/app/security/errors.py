from uuid import uuid4

from starlette.responses import JSONResponse


def problem(status: int, title: str, detail: str, type_: str = "about:blank"):
    """Возвращает ошибку в формате RFC 7807 с correlation_id"""
    cid = str(uuid4())
    return JSONResponse(
        {
            "type": type_,
            "title": title,
            "status": status,
            "detail": detail,
            "correlation_id": cid,
        },
        status_code=status,
    )
