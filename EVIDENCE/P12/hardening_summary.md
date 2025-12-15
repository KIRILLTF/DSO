# Hardening Summary (P12)

## Dockerfile

**До:**
- Использовался `FROM ...:latest`
- Приложение запускалось от root
- Не было HEALTHCHECK
- Были потенциальные уязвимости в базовом образе

**После:**
- `FROM python:3.11-slim` (без `latest`)
- Добавлен непривилегированный пользователь `app`
- Добавлены:
  - `USER app`
  - `HEALTHCHECK`
  - `ENV PYTHONUNBUFFERED=1`
- Используется `--no-cache-dir` при установке пакетов
- Вывод pip — отключён
- Приложение запускается через `CMD ["uvicorn", "app.main:app", ...]`

**Планируется:**
- Протестировать более безопасный базовый образ (например, `slim-bullseye`)
- Использовать multistage для ещё меньшего runtime-образа

---

## IaC (deployment.yaml)

**До:**
- Базовый deployment без ограничений

**После:**
- Прошёл >10 Checkov-проверок (RBAC, ресурсы, TLS, авторизация и др.)
- Установлены:
  - CPU limits
  - RBAC
  - Node/Pod Security Policies
  - Отключён hostIPC
- Нет критичных политик типа `AlwaysAllow`, `hostNetwork`, `hostPID`

**Планируется:**
- Добавить liveness и readiness-пробы
- Разнести deployment/service в отдельные манифесты
