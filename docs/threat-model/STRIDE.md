# STRIDE Analysis — Media Service

| Поток/Элемент | Угроза (STRIDE)       | Риск | Контроль | Ссылка на NFR | Проверка/Артефакт |
|---------------|----------------------|------|----------|---------------|-------------------|
| F1 /login     | S: Spoofing          | R1   | MFA + rate-limit | NFR-01, NFR-04 | e2e + ZAP baseline |
| F1 /login     | T: Tampering         | R2   | HTTPS, input validation | NFR-02 | Integration tests |
| F2 /media     | I: Information leak  | R3   | AuthZ, minimal payload | NFR-02 | Contract tests |
| F3 DB write   | R: Repudiation       | R4   | Audit logging | NFR-03 | Logging verification |
| F4 token     | E: Elevation         | R5   | Token expiration, RBAC | NFR-01 | Unit tests |
| F5 user      | D: Denial of Service | R6   | Rate limit, queue | NFR-04 | Load tests |
