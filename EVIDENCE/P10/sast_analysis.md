# P10 - SAST & Secrets Summary

**Дата сканирования:** 2025-12-06 23:50:06 UTC  
**Workflow run:** [#2](https://github.com/KIRILLTF/DSO/actions/runs/19995993151)

## Результаты сканирования

### Semgrep: 7 предупреждений
1. **GitHub Actions Shell Injection** (1 предупреждение)  
   - Файл: `.github/workflows/ci.yml:180-202`  
   - Правило: `yaml.github-actions.security.run-shell-injection.run-shell-injection`  
   - Описание: Использование `${{ github.event.head_commit.message }}` в run-скрипте

2. **Hardcoded JWT Secrets** (3 предупреждения)  
   - Файлы:  
     - `src/app/api/auth.py:37`  
     - `src/app/api/routes_auth.py:43`  
     - `src/services/auth_service.py:65`  
   - Правило: `python.jwt.security.jwt-hardcode.jwt-python-hardcoded-secret`  
   - CWE: 522 (Insufficiently Protected Credentials)

3. **Weak SHA-224 Hash** (3 предупреждения)  
   - Файлы в `venv/` (vendor-код библиотек pip)  
   - Правило: `python.lang.security.audit.sha224-hash.sha224-hash`  
   - CWE: 327 (Use of a Broken or Risky Cryptographic Algorithm)

### Gitleaks: 0 потенциальных секретов
- Отчёт пустой: `[]`
- Allowlist настроен для исключения тестовых данных

## Анализ findings

### Критические проблемы (требуют действий):
1. **Hardcoded JWT Secrets** — секреты закодированы прямо в коде вместо переменных окружения
2. **GitHub Actions Shell Injection** — потенциальная инъекция через контекст GitHub

### Vendor-код (можно игнорировать):
- **Weak SHA-224 Hash** — находится в папке `venv/` (внешние зависимости)

## Артефакты
- [semgrep.sarif](semgrep.sarif) — полный отчёт Semgrep
- [gitleaks.json](gitleaks.json) — пустой отчёт Gitleaks

## Следующие шаги
1. Перенести JWT секреты из кода в переменные окружения
2. Исправить потенциальную инъекцию в CI скрипте
3. Регулярно запускать SAST и secrets scanning в CI/CD