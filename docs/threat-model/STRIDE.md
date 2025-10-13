
---

## 2️⃣ `STRIDE.md` — Полная таблица угроз

```markdown
# P04 — Threat Modeling: STRIDE

| Поток/Элемент      | Угроза (STRIDE)       | Риск | Контроль                                    | Ссылка на NFR       | Проверка/Артефакт               |
|--------------------|----------------------|------|--------------------------------------------|-------------------|---------------------------------|
| F1 /auth/login     | S: Spoofing           | R1   | MFA + rate-limit на /login                  | NFR-01, NFR-04     | e2e + ZAP baseline             |
| F1 /auth/login     | T: Tampering          | R2   | HTTPS + JWT подпись                          | NFR-02, NFR-03     | unit + security tests           |
| F2 /auth/register  | R: Repudiation        | R3   | Логи регистрации пользователей              | NFR-05             | audit log check                 |
| F3 /media/         | I: Information Leak   | R4   | Авторизация и проверка владельца файла      | NFR-01, NFR-03     | e2e тесты                       |
| F4 /media/{id}     | D: Denial             | R5   | Rate-limit, soft delete                     | NFR-04             | stress test                     |
| F5 /media/{id}     | T: Tampering          | R6   | JWT + проверка владения ресурсом           | NFR-01, NFR-03     | unit + интеграционные тесты     |
| F6 /media/{id}     | R: Repudiation        | R7   | Логи удаления медиа                          | NFR-05             | audit log check                 |
| F3 /media/         | S: Spoofing           | R8   | JWT + проверка прав пользователя           | NFR-01, NFR-04     | unit + e2e                      |
| F4 /media/{id}     | I: Information Leak   | R9   | Ограничение доступа по владельцу           | NFR-01, NFR-03     | e2e + unit                      |
| F5 /media/{id}     | D: Denial             | R10  | Rate-limit + контроль целостности данных   | NFR-04             | stress test                     |
| F6 /media/{id}     | T: Tampering          | R11  | JWT + проверка владельца                    | NFR-01, NFR-03     | unit + интеграционные тесты     |
