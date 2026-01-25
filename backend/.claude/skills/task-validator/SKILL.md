---
name: task-validator
description: 태스크 완료 조건을 검증하고 누락된 항목을 식별하는 스킬. (1) 태스크 완료 선언 전 "완료됐는지 확인해줘" 요청 시, (2) 다음 태스크로 넘어가기 전 검증 시, (3) PR/커밋 전 체크리스트 확인 시 트리거. 완료 조건 대비 현재 상태를 비교하여 누락 항목을 알려줌.
---

# Task Validator

태스크 완료 조건을 검증하고 누락된 항목을 식별한다.

## 검증 항목

### 1. 체크리스트 완료
로드맵의 서브태스크가 모두 완료되었는지

### 2. 완료 조건 충족
정의된 완료 조건(Acceptance Criteria)이 충족되었는지

### 3. 테스트 통과
관련 테스트가 작성되고 통과하는지

### 4. 코드 품질
기본적인 코드 품질 기준 충족 여부

## 워크플로우

### Step 1: 태스크 정보 수집
- 태스크 ID/설명
- 체크리스트 항목
- 완료 조건
- 관련 파일 목록

### Step 2: 현재 상태 확인
- 체크리스트 상태
- 파일 존재 여부
- 테스트 실행 결과

### Step 3: 검증 수행
각 항목별 완료 여부 판단

### Step 4: 결과 보고
완료/미완료 및 누락 항목 안내

## 검증 기준

### 코드 존재 확인
```python
# 파일이 존재하는지
assert os.path.exists("app/services/product.py")

# 함수/클래스가 정의되어 있는지
assert hasattr(ProductService, "get_by_barcode")
```

### 테스트 확인
```bash
# 테스트 파일 존재
ls tests/unit/test_product_service.py

# 테스트 통과
pytest tests/unit/test_product_service.py -v
```

### API 동작 확인
```bash
# 서버 실행 상태에서
curl http://localhost:8000/products/barcode/test

# Swagger 문서 확인
curl http://localhost:8000/openapi.json | jq '.paths["/products/barcode/{barcode}"]'
```

## 출력 형식

### 검증 결과
```markdown
# ✅ 태스크 검증 결과

**태스크**: A-1. OpenAPI 스펙 강화
**검증 시간**: 2026-01-24 15:30

---

## 체크리스트 상태

| 항목 | 상태 | 비고 |
|------|------|------|
| 공통 에러 응답 스키마 정의 | ✅ 완료 | `app/schemas/common.py` |
| 엔드포인트 설명 추가 | ✅ 완료 | 5개 엔드포인트 |
| 요청/응답 예시 추가 | ⚠️ 부분 | 3/5 완료 |
| 에러 응답 스키마 정의 | ❌ 미완료 | |

**진행률**: 75% (3/4)

---

## 완료 조건 검증

| 조건 | 상태 | 확인 방법 |
|------|------|----------|
| /docs에서 모든 API 설명 확인 | ✅ 충족 | 수동 확인 |
| 에러 케이스별 응답 예시 포함 | ❌ 미충족 | 404, 500 누락 |

---

## 테스트 상태

```
pytest tests/ -v --tb=short
========================
5 passed, 0 failed
========================
```

---

## 누락 항목

### 🔴 필수 완료
1. 에러 응답 스키마 정의
   - 파일: `app/schemas/common.py`
   - 내용: 400, 404, 500 에러 응답 스키마

2. 나머지 2개 엔드포인트 예시 추가
   - POST /products
   - PUT /products/{id}

---

## 결론

**상태**: ⚠️ 미완료 (75%)

다음 태스크로 진행하기 전 위 누락 항목을 완료해주세요.
```

### 완료 시
```markdown
# ✅ 태스크 검증 완료

**태스크**: A-1. OpenAPI 스펙 강화
**상태**: ✅ 완료

모든 체크리스트와 완료 조건이 충족되었습니다.

## 요약
- 체크리스트: 4/4 완료
- 완료 조건: 2/2 충족
- 테스트: 5/5 통과

**다음 단계**: 문서 업데이트 후 커밋
```

## 자동 검증 가능 항목

### 파일 존재
```python
required_files = [
    "app/schemas/common.py",
    "app/api/v1/products.py",
    "tests/unit/test_product.py"
]

for f in required_files:
    if not os.path.exists(f):
        print(f"❌ 누락: {f}")
```

### 함수/클래스 존재
```python
from app.schemas.common import ErrorResponse
from app.services.product import ProductService

assert hasattr(ProductService, "get_by_barcode")
```

### 테스트 통과
```bash
pytest tests/unit/test_product_service.py --tb=no -q
```

### 린트 통과
```bash
ruff check app/services/product.py
mypy app/services/product.py
```

## 수동 검증 필요 항목

다음은 자동 검증이 어려워 수동 확인 필요:
- UI/UX 품질
- 문서 가독성
- 코드 설계 적절성
- 비즈니스 로직 정확성

## 검증 실패 시 가이드

### 파일 누락
```markdown
❌ `app/schemas/common.py` 누락

**해결**: 파일 생성 후 ErrorResponse 스키마 정의
```python
# app/schemas/common.py
class ErrorResponse(BaseModel):
    error_code: str
    message: str
```
```

### 테스트 실패
```markdown
❌ 테스트 실패: test_get_by_barcode_not_found

**실패 원인**: None 반환 대신 예외 발생
**해결**: 서비스 로직 수정 또는 테스트 기대값 수정
```

### 완료 조건 미충족
```markdown
❌ 완료 조건 미충족: "P95 응답 시간 100ms 이내"

**현재 상태**: P95 = 150ms
**해결**: 쿼리 최적화 또는 캐싱 적용 필요
```