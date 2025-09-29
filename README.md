
````markdown
# SecDev Course Template

Стартовый шаблон для студенческого репозитория (HSE SecDev 2025).

---

## Быстрый старт (Windows PowerShell)

1. Создаём виртуальное окружение:
```powershell
python -m venv .venv
````

2. Разрешаем выполнение скриптов (если потребуется):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

3. Активируем виртуальное окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Устанавливаем зависимости:

```powershell
pip install -r requirements.txt -r requirements-dev.txt
```

5. Устанавливаем pre-commit hooks:

```powershell
pre-commit install
```

6. Запускаем сервер:

```powershell
uvicorn app.main:app --reload
```

7. Проверяем эндпойнт:

```
http://127.0.0.1:8000/health
```

---

## Ритуал перед PR

Перед Pull Request проверяем код и форматирование:

```powershell
ruff check --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

---

## Тесты

```powershell
pytest -q
```

---

## CI

В репозитории настроен workflow CI (GitHub Actions) — required check для main.
Badge добавится автоматически после загрузки шаблона в GitHub.

---

## Контейнеры

```powershell
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```

---

## Эндпойнты

* `GET /health` → `{"status": "ok"}`
* `POST /items?name=...` — демо-сущность
* `GET /items/{id}`

---

## Формат ошибок

Все ошибки — JSON-обёртка:

```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

---

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.
