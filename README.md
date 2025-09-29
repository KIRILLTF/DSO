````markdown
SecDev Course Template
Стартовый шаблон для студенческого репозитория (HSE SecDev 2025).

Быстрый старт
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
uvicorn app.main:app --reload

Ритуал перед PR
ruff check --fix .
black .
isort .
pytest -q
pre-commit run --all-files

Тесты
pytest -q

CI
В репозитории настроен workflow CI (GitHub Actions) — required check для main. Badge добавится автоматически после загрузки шаблона в GitHub.

Контейнеры
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build

Эндпойнты
GET /health → {"status": "ok"}
POST /items?name=... — демо-сущность
GET /items/{id}

Формат ошибок
Все ошибки — JSON-обёртка:

{
  "error": {"code": "not_found", "message": "item not found"}
}

P02 — Git-процессы и рецензирование
Цель: отработать рабочую модель ветвления, оформление PR по шаблону, содержательное ревью и правила защиты main с обязательными статусами.

### Как работать
1. Создаём ветку от `main`:
```bash
git checkout main
git pull
git checkout -b p02-<short-topic>
````

Пример: `p02-update-readme`

2. Вносим изменения в ветке `p02-*`.

3. Проверяем локально всё зелёное:

```bash
pre-commit run --all-files
ruff check --fix .
black .
isort .
pytest -q
```

4. Открываем PR `p02-* → main`:

* Заполняем шаблон PR (что сделано / как проверял / чек-лист)
* Добавляем ревьюеров
* Ссылка на Issue/задачу (если есть)

5. Исправляем замечания по ревью и ждём зелёного CI.

6. После зелёного CI и аппрувов делаем merge pull request и, при необходимости, ставим тег:

```bash
git checkout main
git pull
git tag P02
git push --tags
```

### Проверка и требования

* Локально все проверки pre-commit должны проходить
* Тесты pytest должны быть зелёными
* Прямые пуши в `main` запрещены
* CI должен быть зелёным перед merge

См. также: SECURITY.md, .pre-commit-config.yaml, .github/workflows/ci.yml.

```
```
****
