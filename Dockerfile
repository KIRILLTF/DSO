# Build stage
FROM python:3.11-slim AS build
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY .. .
# Запуск тестов на этапе сборки
RUN pytest -q --disable-warnings

# Runtime stage
FROM python:3.11-slim
WORKDIR /app

# Создаём непривилегированного пользователя
RUN groupadd -r app && useradd -r -g app app

# Копируем установленные библиотеки из build stage
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin

# Копируем только код приложения
COPY .. .

# Права на файлы для непривилегированного пользователя
RUN chown -R app:app /app

# Задаём пользователя
USER app

# Environment
ENV PYTHONUNBUFFERED=1

# Порт и healthcheck
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
