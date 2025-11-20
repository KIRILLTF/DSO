# tests/test_audit_basic.py


def test_audit_service_basic():
    """Базовый тест аудит сервиса"""
    # Импортируем внутри функции чтобы избежать проблем
    from src.services.audit_service import AuditService

    service = AuditService()
    assert service is not None

    # Простой тест маскирования
    details = {"password": "test", "data": "safe"}
    result = service._sanitize_details(details)
    assert result["password"] == "***MASKED***"
    assert result["data"] == "safe"
