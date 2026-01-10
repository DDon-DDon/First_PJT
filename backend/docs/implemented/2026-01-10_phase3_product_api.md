# 구현 리포트: Phase 3 - 제품 (Product) API

**작성일**: 2026-01-08
**구현 범위**: 제품 조회, 검색, 생성 (관리자) API
**담당자**: Backend Agent (Claude)

---

## 1. 개요

Phase 3에서는 제품(Product) 도메인에 대한 핵심 API를 TDD(Test-Driven Development) 방법론을 적용하여 구현했습니다.
시스템의 가장 기초가 되는 마스터 데이터를 다루며, 바코드 스캔 성능(< 1초)과 관리자 권한 제어가 핵심 요구사항이었습니다.

### 주요 변경 사항 요약
- **API 엔드포인트**: `GET /products`, `GET /products/barcode/{barcode}`, `POST /products` 구현
- **서비스 로직**: 비즈니스 로직 분리 (`ProductService`)
- **스키마 개선**: Pydantic V2 호환성 확보 (`from_attributes`, `alias` 적용)
- **테스트 커버리지**: 성공/실패/권한/중복 케이스 등 7개 테스트 작성 및 통과

---

## 2. 상세 구현 내용

### 2.1 Pydantic 스키마 리팩토링 (`app/schemas/product.py`)

기존 스키마는 SQLAlchemy 모델(snake_case)과 API 응답(camelCase) 간의 매핑이 불완전했습니다.
이를 해결하기 위해 `Field(alias="...")`를 사용하여 명시적으로 매핑을 정의했습니다.

**변경 전**:
```python
class ProductResponse(BaseModel):
    categoryId: UUID  # 모델의 category_id와 매핑되지 않음
    safetyStock: int
```

**변경 후**:
```python
class ProductResponse(BaseModel):
    category_id: UUID = Field(..., alias="categoryId")
    safety_stock: int = Field(..., alias="safetyStock")
    is_active: bool = Field(..., alias="isActive")
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
```
이로써 DB 모델을 `ProductResponse.model_validate(product)`로 변환할 때 자동으로 필드명이 변환됩니다.

### 2.2 서비스 레이어 (`app/services/product.py`)

비즈니스 로직을 API 라우터에서 분리하여 재사용성과 테스트 용이성을 확보했습니다.

- **`get_product_by_barcode`**:
    - `joinedload(Product.category)`를 사용하여 N+1 문제를 방지했습니다.
    - 바코드 인덱스를 활용하여 단건 조회 성능을 최적화했습니다.
- **`list_products`**:
    - 동적 쿼리 빌딩: `search` 파라미터가 있을 때만 `ilike` 조건이 추가됩니다.
    - 페이지네이션: `offset`과 `limit`을 적용하고, 전체 개수(`total`)를 별도 카운트 쿼리로 계산했습니다.
- **`create_product`**:
    - **유효성 검증**: 바코드 중복 체크(`ConflictException`), 카테고리 존재 여부 확인(`NotFoundException`)을 수행합니다.
    - UUID 변환: 문자열로 들어온 ID를 UUID 객체로 안전하게 변환합니다.

### 2.3 API 라우터 (`app/api/v1/products.py`)

FastAPI의 `APIRouter`를 사용하여 엔드포인트를 정의했습니다.

- **`GET /barcode/{barcode}`**:
    - 제품이 없으면 `404 Not Found`를 명확히 반환합니다.
- **`GET /`**:
    - Query Parameter Validation: `page >= 1`, `limit <= 100` 등의 제약조건을 `Query` 객체로 설정했습니다.
    - 응답 형식: `items`와 `pagination` 메타데이터를 포함한 구조로 반환합니다.
- **`POST /`**:
    - **권한 제어**: `get_current_user` 의존성을 주입받아 `user.role != 'ADMIN'`인 경우 `403 Forbidden`을 발생시킵니다.
    - 상태 코드: 성공 시 `201 Created`를 반환합니다.

### 2.4 테스트 코드 (`tests/test_products.py`)

`pytest`와 `httpx`를 사용하여 비동기 통합 테스트를 작성했습니다.

| 테스트 케이스 | 설명 | 결과 |
|--------------|------|------|
| `test_get_product_by_barcode_success` | 존재하는 바코드로 조회 시 200 OK 및 데이터 검증 | ✅ Pass |
| `test_get_product_by_barcode_not_found` | 없는 바코드로 조회 시 404 Not Found | ✅ Pass |
| `test_list_products` | 페이지네이션(page, limit) 동작 및 Total Count 검증 | ✅ Pass |
| `test_list_products_filter` | 검색어 및 카테고리 필터링 동작 검증 | ✅ Pass |
| `test_create_product_admin` | ADMIN 권한으로 제품 생성 성공 (201) | ✅ Pass |
| `test_create_product_worker_fail` | WORKER 권한으로 제품 생성 실패 (403) | ✅ Pass |
| `test_create_product_duplicate_barcode` | 중복 바코드 생성 시도 시 실패 (409) | ✅ Pass |

---

## 3. 기술적 이슈 및 해결

### 이슈 1: Pydantic V2 Validation Error
- **증상**: API 응답 시 `Field required` 에러 발생.
- **원인**: Pydantic 스키마의 필드명(camelCase)과 SQLAlchemy 모델의 속성명(snake_case)이 일치하지 않음.
- **해결**: 스키마 필드명을 snake_case로 변경하고 `alias` 속성을 사용하여 JSON 출력 시 camelCase가 되도록 수정함.

### 이슈 2: SQLAlchemy Relationship 에러
- **증상**: `Product` 모델 로드 시 `TypeError: RelationshipProperty... got unexpected keyword 'comment'` 발생.
- **원인**: `relationship()` 함수는 `comment` 인자를 지원하지 않음 (Phase 1 모델 정의 시 실수).
- **해결**: `Product` 모델에서 `comment` 인자 제거.

### 이슈 3: Mypy 타입 힌트 오류
- **증상**: `list_products` 함수의 리턴 타입 불일치 (`Sequence` vs `List`).
- **원인**: SQLAlchemy의 `scalars().all()`은 `Sequence` 타입을 반환함.
- **해결**: 리턴 타입 힌트를 `Tuple[Sequence[Product], int]`로 수정.

---

## 4. 향후 계획

- **Phase 4 (재고 API)**: 구현된 `Product`를 기반으로 매장별 재고(`CurrentStock`) 조회 API 구현 예정.
- **인증 연동**: 현재 Mocking된 `get_current_user`를 Phase 2 완료 후 실제 JWT 인증 로직으로 교체 필요.
