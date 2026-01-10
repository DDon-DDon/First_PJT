# 개발 지시서: Phase 4 - 재고 (Inventory) 조회 API 구현

**작성일**: 2026-01-08
**대상 에이전트**: Backend Developer Agent
**목표**: 현재고(`CurrentStock`) 조회 및 상태 계산(`status`) 기능을 구현한다.

---

## 1. 개요 및 컨텍스트

이전 단계에서 `Product` API가 구현되었습니다. 이번 **Phase 4**에서는 각 매장에 쌓인 재고를 조회하는 기능을 구현합니다.
특히, 재고 수량에 따라 **LOW / NORMAL / GOOD** 상태를 동적으로 계산해서 클라이언트에 내려주는 것이 핵심입니다.

**중요 요구사항**:
- **복합 키 조회**: `CurrentStock`은 `product_id` + `store_id`가 PK입니다.
- **상태 계산 로직**: `Product.safety_stock`을 기준으로 상태를 판단해야 합니다.
- **권한 분리**:
    - **WORKER**: 본인이 배정된 매장의 재고만 조회 가능.
    - **ADMIN**: 모든 매장, 또는 특정 매장을 선택하여 조회 가능.

---

## 2. 작업 상세 내용

### Task 1: 단위 테스트 작성 (`tests/test_inventory.py`)
조회 로직 검증을 위한 테스트를 먼저 작성하세요.

1.  **재고 상태 계산 테스트**
    *   `test_get_stock_status`:
        *   재고 < 안전재고 -> "LOW"
        *   안전재고 <= 재고 < 안전재고*2 -> "NORMAL"
        *   재고 >= 안전재고*2 -> "GOOD"
2.  **재고 목록 조회 테스트**
    *   `test_list_stocks_worker`: 작업자 토큰으로 요청 시 본인 매장 재고만 반환하는지 확인.
    *   `test_list_stocks_admin`: 관리자가 `store_id` 파라미터로 특정 매장 재고 조회 확인.
    *   `test_list_stocks_status_filter`: `status=LOW` 파라미터로 필터링되는지 확인.

### Task 2: 서비스 레이어 구현 (`app/services/inventory.py`)
재고 조회 및 비즈니스 로직을 구현하세요.

*   **`get_stock_status(quantity: int, safety_stock: int) -> str`**
    *   순수 함수로 구현하여 테스트 용이성 확보.
*   **`get_current_stocks(db: AsyncSession, params: InventoryFilterParams, user: User)`**
    *   `CurrentStock`, `Product`, `Store` 조인 조회.
    *   유저 권한(`user.role`)에 따라 `store_id` 필터링 강제 적용 로직 포함.
    *   결과 반환 시 `status` 필드를 계산하여 주입.

### Task 3: API 엔드포인트 구현 (`app/api/v1/inventory.py`)
FastAPI 라우터를 구현하세요.

*   **`GET /inventory/stocks`**
    *   Query Params: `store_id` (Admin only), `category_id`, `status` (`LOW`|`NORMAL`|`GOOD`), `page`, `limit`
    *   Response Model: `StockListResponse` (items, pagination)
        *   Item Model: product(간략 정보), store(간략 정보), quantity, status, last_alerted_at
*   **`GET /inventory/stocks/{productId}`** (ADMIN Only)
    *   특정 제품의 모든 매장 재고 현황.
    *   Response: `ProductStockDetailResponse` (product info + list of store stocks)

---

## 3. 참고 자료

### 관련 파일 경로
- 모델: `backend/app/models/stock.py`, `backend/app/models/store.py`
- 스키마: `backend/app/schemas/stock.py` (또는 inventory.py)

### 상태 계산 로직 (PRD 참조)
```python
def get_stock_status(quantity, safety_stock):
    if quantity < safety_stock: return "LOW"
    if quantity < safety_stock * 2: return "NORMAL"
    return "GOOD"
```

---

## 4. 완료 조건 (Definition of Done)
1. `tests/test_inventory.py` 테스트 통과.
2. WORKER가 다른 매장의 재고를 조회할 수 없도록 권한 제어가 동작해야 함.
3. `status` 필드가 올바르게 계산되어 응답에 포함되어야 함.
