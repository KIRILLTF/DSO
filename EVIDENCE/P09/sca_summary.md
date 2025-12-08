# SCA Summary

## Scan Metadata
- Commit: [7c0fea7dd4e189b2d513414f9a858dbfd27024d0](https://github.com/KIRILLTF/DSO/commit/7c0fea7dd4e189b2d513414f9a858dbfd27024d0)
- Branch: p09-sbom-sca
- Workflow run: [#20035240532](https://github.com/KIRILLTF/DSO/actions/runs/20035240532)
- Generated: 2025-12-08 16:30:19 UTC
- Tools: Application:   syft
Version:       1.38.0
BuildDate:     2025-11-17T17:42:49Z
GitCommit:     a033ae525f6c7ef937c6f49513e3403f07a1d6c0
GitDescription: v1.38.0
Platform:      linux/amd64
GoVersion:     go1.25.4
Compiler:      gc
SchemaVersion: 16.1.0, Application:         grype
Version:             0.104.1
BuildDate:           2025-11-24T16:11:42Z
GitCommit:           39f7fa17af2739cafe9b27176d4a68f7c05f21c1
GitDescription:      v0.104.1
Platform:            linux/amd64
GoVersion:           go1.25.4
Compiler:            gc
Syft Version:        v1.38.0
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
