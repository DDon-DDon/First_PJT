# 개발 지시서: Phase 3 - 제품 (Product) API 구현

**작성일**: 2026-01-08
**대상 에이전트**: Backend Developer Agent
**목표**: `Product` 도메인에 대한 조회, 검색, 생성 기능을 TDD 방식으로 구현한다.

---

## 1. 개요 및 컨텍스트

현재 `Phase 1`이 완료되어 데이터베이스 모델(`Product`, `Category` 등)과 Pydantic 스키마는 이미 구현되어 있습니다.
이번 작업은 **Phase 3**에 해당하며, 실제 비즈니스 로직(Service)과 API 엔드포인트(Router)를 구현하고 이를 테스트하는 것이 목표입니다.

**중요 요구사항**:
- **성능**: 바코드 조회는 반드시 **1초 이내**에 응답해야 합니다. (인덱스 활용)
- **권한**: 제품 생성(`POST /products`)은 **ADMIN** 권한을 가진 사용자만 가능합니다. (현재 Auth 구현이 미뤄졌으므로, Mock user 또는 의존성 주입 시 role을 주입하여 테스트)
- **스타일**: 비동기(`async/await`) 처리, Type Hinting, Pydantic 검증을 엄격히 준수합니다.

---

## 2. 작업 상세 내용

### Task 1: 단위 테스트 작성 (`tests/test_products.py`)
서비스 및 API 구현 전, 실패하는 테스트 케이스를 먼저 작성하세요.

1.  **바코드 조회 테스트**
    *   `test_get_product_by_barcode_success`: 존재하는 바코드로 조회 시 제품 정보 반환 확인.
    *   `test_get_product_by_barcode_not_found`: 없는 바코드 조회 시 404 에러 확인.
2.  **제품 목록 조회 테스트**
    *   `test_list_products`: 페이지네이션(`page`, `limit`) 동작 확인.
    *   `test_list_products_filter`: 검색어(`search`) 및 카테고리(`category_id`) 필터링 확인.
3.  **제품 생성 테스트 (권한)**
    *   `test_create_product_admin`: `role="ADMIN"`일 때 정상 생성 확인.
    *   `test_create_product_worker_fail`: `role="WORKER"`일 때 403 Forbidden 확인.
    *   `test_create_product_duplicate_barcode`: 이미 존재하는 바코드로 생성 시도 시 400/409 에러 확인.

### Task 2: 서비스 레이어 구현 (`app/services/product.py`)
비즈니스 로직을 담당하는 `ProductService` 클래스(또는 함수 집합)를 구현하세요.

*   **`get_product_by_barcode(db: AsyncSession, barcode: str)`**
    *   DB에서 바코드로 단일 조회.
    *   `select(Product).where(Product.barcode == barcode)`
*   **`list_products(db: AsyncSession, params: ProductFilterParams)`**
    *   `Product`와 `Category`를 조인(Joined Load)하여 조회.
    *   동적 쿼리 작성 (검색어가 있으면 `ilike`, 카테고리가 있으면 `eq`).
    *   Total Count 계산 및 Pagination 적용.
*   **`create_product(db: AsyncSession, data: ProductCreate)`**
    *   바코드 중복 체크.
    *   `Product` 인스턴스 생성 및 `db.add`, `db.commit`.

### Task 3: API 엔드포인트 구현 (`app/api/v1/products.py`)
FastAPI 라우터를 정의하고 서비스 함수를 연결하세요.

*   **`GET /products/barcode/{barcode}`**
    *   Response Model: `ProductResponse`
    *   Service 호출 결과가 없으면 `HTTPException(404)` 발생.
*   **`GET /products`**
    *   Query Parameters: `page`, `limit`, `search`, `category_id`
    *   Response Model: `ProductListResponse` (items, pagination 포함)
*   **`POST /products`**
    *   Dependency: `get_current_user` (현재 Auth 미구현이므로 Mocking 가능한 구조로 작성하거나, 임시 의존성 사용)
    *   `current_user.role != 'ADMIN'`이면 `HTTPException(403)` 발생.
    *   Response Model: `ProductResponse` (status code 201)

---

## 3. 참고 자료

### 관련 파일 경로
- 모델: `backend/app/models/product.py`, `backend/app/models/category.py`
- 스키마: `backend/app/schemas/product.py`
- 공통 스키마: `backend/app/schemas/common.py` (Pagination 등)

### 데이터 구조 예시 (Product)
```python
class Product(Base):
    # ...
    barcode: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    safety_stock: Mapped[int] = mapped_column(default=10)
    # ...
```

---

## 4. 완료 조건 (Definition of Done)
1. `tests/test_products.py`의 모든 테스트가 통과해야 한다.
2. `ruff check .` 및 `mypy .` 검사를 통과해야 한다.
3. 바코드 조회 API 응답 시간이 로컬 환경 기준 평균 100ms 이내여야 한다.
