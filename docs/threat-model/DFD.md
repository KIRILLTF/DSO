# Data Flow Diagram (DFD) — Media Catalog Service

## Overview

Диаграмма отражает потоки данных между пользователем, API Gateway, сервисами аутентификации и управления медиа, а также хранилищем данных и файлов.
Границы доверия (Trust Boundaries) выделены для Edge и Core уровней системы.

---

## DFD — Main Scenario

```mermaid
flowchart LR
    %% External
    subgraph External["External Entity"]
        U[ User / Client App]
    end

    %% Edge layer
    subgraph Edge["Trust Boundary: Edge Layer (FastAPI / Gateway)"]
        GW[ API Gateway / FastAPI Router]
        AUTH[ Auth Service]
        MEDIA[ Media Service]
    end

    %% Core layer
    subgraph Core["Trust Boundary: Core Layer (Persistent Storage)"]
        DB[( PostgreSQL - media.db)]
        FS[( Media Files Storage)]
    end

    %% Flows
    U -->|F1: HTTPS POST /auth/register| GW
    GW -->|F2: Forward registration| AUTH
    AUTH -->|F3: Store user with argon2| DB

    U -->|F4: HTTPS POST /auth/login| GW
    GW -->|F5: Validate credentials| AUTH
    AUTH -->|F6: Return JWT access token| U

    U -->|F7: HTTPS POST /media/upload| GW
    GW -->|F8: Forward upload request| MEDIA
    MEDIA -->|F9: Write metadata| DB
    MEDIA -->|F10: Save file| FS
    MEDIA -->|F11: Return file info| U

    U -->|F12: HTTPS GET /media/list| GW
    GW -->|F13: Forward request| MEDIA
    MEDIA -->|F14: Read metadata| DB
    MEDIA -->|F15: Return media list| U

    %% Styles
    style GW stroke-width:2px,stroke:#1E90FF
    style AUTH stroke-dasharray:5 5,stroke:#FF8C00
    style MEDIA stroke-dasharray:5 5,stroke:#32CD32
    style DB fill:#F3F3F3,stroke:#666
    style FS fill:#F3F3F3,stroke:#666
```


| ID потока | Направление              | Протокол     | Конечная точка     | Описание |
|------------|--------------------------|---------------|--------------------|-----------|
| F1 | Пользователь → Шлюз | HTTPS POST | /auth/register | Запрос регистрации с учётными данными |
| F2 | Шлюз → Аутентификация | Внутренний | – | Передача данных регистрации |
| F3 | Аутентификация → БД | SQL INSERT | – | Сохранение пользователя с хешем пароля (argon2id) |
| F4 | Пользователь → Шлюз | HTTPS POST | /auth/login | Запрос входа с учётными данными |
| F5 | Шлюз → Аутентификация | Внутренний | – | Проверка учётных данных пользователя |
| F6 | Аутентификация → Пользователь | HTTPS Response | – | Возврат JWT access token |


| ID потока | Направление              | Протокол     | Конечная точка     | Описание |
|------------|--------------------------|---------------|--------------------|-----------|
| F7 | Пользователь → Шлюз | HTTPS POST | /media/upload | Загрузка медиафайла (JWT аутентификация) |
| F8 | Шлюз → Медиа | Внутренний | – | Передача запроса на загрузку |
| F9 | Медиа → БД | SQL INSERT | – | Запись метаданных файла в PostgreSQL |
| F10 | Медиа → Хранилище | Запись файла | – | Сохранение медиафайла в хранилище |
| F11 | Медиа → Пользователь | HTTPS Response | – | Возврат информации о файле и URL |
| F12 | Пользователь → Шлюз | HTTPS GET | /media/list | Запрос списка медиа (JWT аутентификация) |
| F13 | Шлюз → Медиа | Внутренний | – | Передача запроса списка |
| F14 | Медиа → БД | SQL SELECT | – | Чтение метаданных из базы данных |
| F15 | Медиа → Пользователь | HTTPS Response | – | Возврат списка медиафайлов |
