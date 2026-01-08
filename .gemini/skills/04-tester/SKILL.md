---
name: Quality Gate Tester
description: 자동화 테스트 + 품질 게이트 (E2E & 성능 테스트 포함)
keywords: ["테스트", "test", "qa", "검증", "품질"]
tools: ["bash", "run_command", "view_file"]
---

# 🧪 테스트 & 품질 검증 (Expanded)

## 🏃‍♂️ 테스트 스위트 (Execution)
```bash
# 1. 단위 및 통합 테스트 (Pytest)
pytest src/tests/ -v --cov=src --cov-report=term-missing

# 2. 정적 분석 (Static Analysis)
bandit -r src/ -ll

# 3. 브라우저/E2E 테스트 (Playwright)
pytest tests/e2e/

# 4. 부하 테스트 (Locust)
locust -f tests/performance/locustfile.py --headless -u 100 -r 10 -t 1m
```

## 📊 품질 기준 (Quality Gate Metrics)
| 항목 | 최소 기준 | 현재 상태 |
| :--- | :---: | :--- |
| **Test Coverage** | 80% 이상 | - |
| **Critical Bugs** | 0건 | - |
| **Response Time** | P95 < 300ms | - |
| **Security Risk** | Low 이하 | - |

## 🧩 에지 케이스 체크리스트
- [ ] 대량 데이터 처리 시 메모리 사용량
- [ ] 네트워크 지연 및 타임아웃 처리
- [ ] 입력값 유효성 검사 (XSS, SQL Injection 방지)

**실패 시**: 상세 로그를 분석하여 `coder`에게 수정 제안을 작성하고 재실행하세요.
**성공 시**: `reviewer` 스킬을 통해 최종 검토를 요청하세요.