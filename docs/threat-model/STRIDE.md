# STRIDE Threat Model

| Поток/Элемент | STRIDE Категория | Угроза | Контроль | Ссылка на NFR |
|----------------|------------------|---------|-----------|----------------|
| F1 | Spoofing | Подмена пользователя | JWT + bcrypt | NFR-01 |
| F2 | Information Disclosure | Утечка токена | HTTPS + Expiry | NFR-02 |
| F3 | Tampering | Изменение файла | Hash validation | NFR-03 |
| F4 | Denial of Service | Перегрузка API | Rate limit | NFR-04 |
| F5 | Elevation of Privilege | Доступ к чужим данным | Owner-check | NFR-05 |
