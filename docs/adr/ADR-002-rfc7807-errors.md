# ADR-002: Формат ошибок RFC 7807 с correlation_id

## Context
Ошибки при загрузке или доступе к медиа должны возвращаться в безопасном формате.
Ранее возвращались «сырые» исключения, раскрывающие внутренние пути и стек.

## Decision
- Использовать единый метод `problem()` для формирования ошибок по RFC 7807.
- Каждый ответ содержит поля `type`, `title`, `status`, `detail`, `correlation_id`.
- Ошибки не раскрывают внутренние пути, только коды и описание.
- Все вызовы FastAPI обёрнуты middleware, возвращающей `JSONResponse`.

## Consequences
+ Безопасные, понятные пользователю ошибки.
+ Легче трассировать проблемы через `correlation_id`.
– Добавление middleware требует рефакторинга ошибок.

## Security impact
Закрывает риск R2 (Information Disclosure).
Поддерживает NFR-03 (Error Handling).

## Links
- NFR-03, R2
- `tests/test_media_security.py::test_problem_format`
