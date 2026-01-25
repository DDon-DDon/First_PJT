# 계약 테스트 (Contract Testing)

Schemathesis를 사용한 OpenAPI 스키마 기반 계약 테스트입니다.

## 개념

계약 테스트는 API가 정의된 스펙(OpenAPI)을 준수하는지 자동으로 검증합니다:
- **응답 스키마 검증**: 실제 응답이 정의된 스키마와 일치하는지
- **상태 코드 검증**: 정의된 상태 코드만 반환하는지
- **필수 필드 검증**: 필수 필드가 누락되지 않았는지
- **타입 검증**: 필드 타입이 스펙과 일치하는지

## 설치

```bash
uv sync --group dev
```

## 실행 방법

### pytest로 실행

```bash
uv run pytest tests/contract/ -v
```

### Schemathesis CLI로 실행 (더 상세한 출력)

```bash
# 서버 실행 중인 경우
uv run schemathesis run http://localhost:8000/openapi.json \
    --checks all \
    --workers 4

# 특정 엔드포인트만 테스트
uv run schemathesis run http://localhost:8000/openapi.json \
    --endpoint "/api/v1/products" \
    --checks all
```

## 검증 항목

| 검증 | 설명 |
|------|------|
| `not_a_server_error` | 5xx 에러가 발생하지 않는지 |
| `status_code_conformance` | 응답 상태 코드가 스펙에 정의되어 있는지 |
| `content_type_conformance` | Content-Type이 스펙과 일치하는지 |
| `response_schema_conformance` | 응답 본문이 스키마와 일치하는지 |

## CI/CD 통합

```yaml
# GitHub Actions 예시
contract-test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: pip install schemathesis
    - name: Run contract tests
      run: |
        schemathesis run http://localhost:8000/openapi.json \
          --checks all \
          --workers 4
```

## 주의사항

1. **인증 필요 엔드포인트**: `--header "Authorization: Bearer <token>"` 추가
2. **데이터 의존성**: 테스트 데이터가 필요한 엔드포인트는 사전 시드 필요
3. **부작용**: POST/PUT/DELETE 테스트 시 실제 데이터가 변경될 수 있음
