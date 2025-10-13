# P04 — Threat Modeling: DFD

## Контекстная диаграмма сервиса

```mermaid
flowchart TD
  %% Внешние участники
  Client[External Client] -->|F1: HTTPS Login| GW[API Gateway]
  Client -->|F2: HTTPS Registration| GW
  Client -->|F3: Upload Media| GW
  Client -->|F4: Get Media| GW
  Client -->|F5: Update Media| GW
  Client -->|F6: Delete Media| GW

  %% Edge доверенная зона
  subgraph Edge[Trust Boundary: Edge Services]
    GW --> Auth[Auth Service]
    GW --> Media[Media Service]
  end

  %% Core доверенная зона
  subgraph Core[Trust Boundary: Core]
    Auth --> DB_Users[(User DB)]
    Media --> DB_Media[(Media DB)]
  end

  %% Протоколы и каналы
  style GW stroke-width:3px
  style Auth stroke-dasharray: 5 5
  style Media stroke-dasharray: 5 5
  style DB_Users fill:#f9f,stroke:#333,stroke-width:2px
  style DB_Media fill:#bbf,stroke:#333,stroke-width:2px

  %% Пронумерованные потоки
  %% F1–F6 уже проставлены выше
Описание доверенных зон:

Edge (Edge Services) — API Gateway, Auth Service, Media Service. Контролируемая зона, проверка JWT, CORS, rate-limiting.

Core (Core Services) — базы данных пользователей и медиа. Хранение данных, управление доступом.

Внешние участники — пользователи/клиенты, которые используют фронтенд или внешние приложения.

Потоки F1–F6:

F1 — клиент логин /auth/login

F2 — регистрация /auth/register

F3 — загрузка медиа /media/

F4 — чтение медиа /media/{id}

F5 — обновление медиа /media/{id}

F6 — удаление медиа /media/{id}
