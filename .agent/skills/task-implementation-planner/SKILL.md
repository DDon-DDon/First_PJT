---
name: task-implementation-planner
description: 단일 태스크를 구현 가능한 상세 계획으로 변환하는 스킬. (1) 태스크 구현 시작 전 "어떻게 구현해?", "구현 계획 세워줘" 요청 시, (2) 로드맵의 특정 태스크를 실제로 착수할 때, (3) 코드 작성 전 파일/함수 구조를 미리 설계할 때 트리거. 레퍼런스 문서와 기존 코드를 분석하여 수정할 파일, 추가할 함수, 구현 순서를 상세히 계획함.
---

# Task Implementation Planner

단일 태스크를 구체적인 구현 계획으로 변환한다. 어떤 파일을 수정하고, 어떤 함수를 추가하며, 어떤 순서로 구현할지 상세히 계획.

## 핵심 원칙

### 좋은 구현 계획의 조건
1. **구체적**: "서비스 구현" ❌ → "`app/services/product.py`에 `get_by_barcode()` 메서드 추가" ✅
2. **순서가 명확**: 의존성 고려한 구현 순서
3. **테스트 포함**: 구현과 함께 테스트 계획
4. **검증 가능**: 각 단계 완료 확인 방법 명시

## 워크플로우

### Step 1: 태스크 분석
입력 정보 확인:
- 태스크 설명 (로드맵에서)
- 관련 레퍼런스 문서 (PRD, API 명세 등)
- 기존 코드베이스 구조
- 완료 조건

### Step 2: 영향 범위 파악
분석할 내용:
- 수정이 필요한 기존 파일
- 새로 생성할 파일
- 의존하는 모듈/패키지
- 영향받는 테스트

### Step 3: 구현 단계 설계
단계별로 분해:
```
1. 스키마/타입 정의 (의존성 없음)
2. 데이터 레이어 (모델, 쿼리)
3. 비즈니스 로직 (서비스)
4. API 레이어 (라우터, 컨트롤러)
5. 테스트
```

### Step 4: 상세 계획 문서 생성

## 출력 형식

### 구현 계획 구조
```markdown
# [태스크명] 구현 계획

**태스크**: [태스크 ID 및 설명]
**예상 시간**: X시간
**작성일**: YYYY-MM-DD

---

## 개요

[태스크가 달성하려는 것 1-2문장]

## 영향 범위

### 수정할 파일
| 파일 | 변경 내용 |
|------|----------|
| `app/schemas/product.py` | `ProductResponse` 스키마 추가 |
| `app/services/product.py` | `get_by_barcode()` 메서드 추가 |

### 새로 생성할 파일
| 파일 | 용도 |
|------|------|
| `tests/unit/test_product_service.py` | 서비스 단위 테스트 |

### 의존성
- 기존: `app/models/product.py` (Product 모델)
- 신규: 없음

---

## 구현 단계

### 1단계: 스키마 정의
**파일**: `app/schemas/product.py`

```python
class ProductResponse(BaseModel):
    id: UUID
    barcode: str
    name: str
    # ...
```

**확인**: import 에러 없이 서버 시작

### 2단계: 서비스 구현
**파일**: `app/services/product.py`

```python
async def get_by_barcode(self, barcode: str) -> Product | None:
    """바코드로 제품 조회"""
    # 구현 내용
```

**확인**: 단위 테스트 통과

### 3단계: 라우터 구현
**파일**: `app/api/v1/products.py`

```python
@router.get("/barcode/{barcode}")
async def get_product_by_barcode(...):
    # 구현 내용
```

**확인**: `/docs`에서 엔드포인트 확인

### 4단계: 테스트 작성
**파일**: `tests/unit/test_product_service.py`

테스트 케이스:
- 존재하는 바코드 조회 → 제품 반환
- 존재하지 않는 바코드 → None 반환
- 잘못된 형식 바코드 → ValidationError

---

## 완료 체크리스트

- [ ] 1단계: 스키마 정의 완료
- [ ] 2단계: 서비스 구현 완료
- [ ] 3단계: 라우터 구현 완료
- [ ] 4단계: 테스트 작성 완료
- [ ] 전체 테스트 통과
- [ ] 코드 리뷰 (셀프)

---

## 참고

- API 명세: `references/api-spec.md#product-barcode`
- 기존 유사 코드: `app/services/inventory.py`
```

## 구현 순서 원칙

### 의존성 기반 순서
```
1. 타입/스키마 (다른 것에 의존 안 함)
   └── Pydantic 모델, TypedDict, Enum
   
2. 데이터 레이어 (타입에만 의존)
   └── ORM 모델, Repository, 쿼리
   
3. 비즈니스 로직 (데이터 레이어에 의존)
   └── Service 클래스, 유틸리티 함수
   
4. API 레이어 (비즈니스 로직에 의존)
   └── Router, Controller, Middleware
   
5. 테스트 (모든 것에 의존)
   └── 단위 테스트, 통합 테스트
```

### 점진적 검증
각 단계 완료 후 확인:
- **1단계 후**: `python -c "from app.schemas.product import ProductResponse"`
- **2단계 후**: `pytest tests/unit/test_product_service.py -v`
- **3단계 후**: 서버 실행 후 `/docs` 확인
- **4단계 후**: `pytest --cov`

## 코드 스니펫 작성 가이드

### 스니펫 포함 기준
- 새로운 패턴이거나 팀에서 처음 사용하는 경우
- 복잡한 로직이 필요한 경우
- 기존 코드와 일관성이 중요한 경우

### 스니펫 생략 기준
- 이미 유사한 코드가 프로젝트에 있는 경우 → "기존 `xxx.py` 참고" 로 대체
- 단순 CRUD인 경우

## 참고 파일

- `references/implementation-checklist.md`: 구현 단계별 체크리스트