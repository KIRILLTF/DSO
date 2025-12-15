# SCA Summary

## Scan Metadata
- Commit: [062169d3372abbafb92ddf7e1ed2c856e2f2b172](https://github.com/KIRILLTF/DSO/commit/062169d3372abbafb92ddf7e1ed2c856e2f2b172)
- Branch: main
- Workflow run: [#20243780285](https://github.com/KIRILLTF/DSO/actions/runs/20243780285)
- Generated: 2025-12-15 18:50:39 UTC
- Tools: Application:   syft
Version:       1.38.2
BuildDate:     2025-12-09T21:48:47Z
GitCommit:     bfe63f83dbaea88e22a5cfcd7d704c034c953730
GitDescription: v1.38.2
Platform:      linux/amd64
GoVersion:     go1.25.4
Compiler:      gc
SchemaVersion: 16.1.0, Application:         grype
Version:             0.104.2
BuildDate:           2025-12-09T23:03:07Z
GitCommit:           b47060229fe05c654a7f0615a131db6cb3bc27f6
GitDescription:      v0.104.2
Platform:            linux/amd64
GoVersion:           go1.25.4
Compiler:            gc
Syft Version:        v1.38.2
Supported DB Schema: 6

## Vulnerability Summary
| Severity | Count |
|----------|-------|
| Critical | 3 |
| High | 28 |
| Medium | 27 |
| Low | 8 |
| Unknown | 0 |

## Top Vulnerabilities (High+)
| CVE ID | Package | Version | Severity |
|--------|---------|---------|----------|
| CVE-2024-6232 | Python | 3.12.0 | High |
| CVE-2024-6232 | Python | 3.12.0 | High |
| GHSA-2jv5-9r88-3w3p | python-multipart | 0.0.6 | High |
| CVE-2024-4032 | Python | 3.12.0 | High |
| CVE-2024-4032 | Python | 3.12.0 | High |
| CVE-2024-7592 | Python | 3.12.0 | High |
| CVE-2024-7592 | Python | 3.12.0 | High |
| GHSA-6c5p-j8vq-pqhj | python-jose | 3.3.0 | Critical |
| CVE-2024-0397 | Python | 3.12.0 | High |
| CVE-2024-0397 | Python | 3.12.0 | High |

## Action Plan
### Immediate Actions (Critical: 3)
1. Анализ всех Critical уязвимостей
2. Обновление зависимостей до безопасных версий
3. Проверить waivers в [policy/waivers.yml](../../policy/waivers.yml)
### Near-term Actions (High: 28)
1. Обновление в течение следующего спринта
2. Оценка рисков для каждого CVE

## Next Steps
1. Просмотреть полный отчет: [sca_report.json](./sca_report.json)
2. Обновить зависимости через PR
3. Проверить актуальность waivers в [policy/waivers.yml](../../policy/waivers.yml)
