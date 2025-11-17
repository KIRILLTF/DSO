# src/app/main.py (дополнение)
import logging
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.app.api.routes_auth import router as auth_router
from src.app.api.routes_media import router as media_router
from src.app.security.errors import http_exception_handler, validation_exception_handler
from src.database import init_db

app = FastAPI(title="My Project")

# Инициализация базы
init_db()

# Регистрируем обработчики ошибок RFC 7807
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключаем маршруты
app.include_router(auth_router, tags=["auth"])
app.include_router(media_router, tags=["media"])


# Security middleware с заголовками
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    # Security headers
    security_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    # Добавляем security headers к существующим
    for header, value in security_headers.items():
        response.headers.setdefault(header, value)

    return response


# Сохраняем существующий middleware для request_id
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    response = await call_next(request)
    return response


class AuditService:
    def __init__(self):
        self.logger = logging.getLogger("security_audit")
        # Настраиваем handler для security логов
        handler = logging.FileHandler("security_audit.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_security_event(
        self, event_type: str, user_id: int = None, details: dict = None
    ):
        """Логирование security событий без PII"""
        log_data = {
            "event_type": event_type,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "details": self._sanitize_details(details) if details else {},
        }
        self.logger.info(f"Security event: {log_data}")

    def _sanitize_details(self, details: dict) -> dict:
        """Удаляет PII из деталей логов"""
        sensitive_fields = {"password", "token", "email", "credit_card", "secret"}
        sanitized = {}
        for k, v in details.items():
            if k in sensitive_fields:
                sanitized[k] = "***MASKED***"
            elif isinstance(v, str) and any(
                field in k.lower() for field in sensitive_fields
            ):
                sanitized[k] = "***MASKED***"
            else:
                sanitized[k] = v
        return sanitized


# Глобальный экземпляр для использования
audit_logger = AuditService()
