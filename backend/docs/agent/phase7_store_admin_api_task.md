# 개발 지시서: Phase 7 - 매장/카테고리 및 관리자 API 구현

**작성일**: 2026-01-08
**대상 에이전트**: Backend Developer Agent
**목표**: 매장(`Store`), 카테고리(`Category`) 조회 API와 관리자용 리포트(안전재고 알림, 엑셀 다운로드)를 구현한다.

---

## 1. 개요 및 컨텍스트

기본적인 CRUD 외에 프론트엔드 셀렉트 박스(Select Box) 등에 사용될 기초 데이터 API와, 관리자가 재고 부족 현황을 파악하고 엑셀로 내려받을 수 있는 기능을 제공합니다.

**중요 요구사항**:
- **관리자 전용 기능**: 재고 부족 알림 조회 및 엑셀 다운로드는 **ADMIN** 권한이 필수입니다.
- **엑셀 내보내기**: Python 라이브러리(`openpyxl` 또는 `pandas`)를 사용하여 `.xlsx` 포맷을 생성, 스트리밍 응답으로 반환해야 합니다.

---

## 2. 작업 상세 내용

### Task 1: 기초 데이터 API 구현 (`app/api/v1/stores.py`, `categories.py`)
별도의 복잡한 비즈니스 로직 없이, DB 조회 후 리스트를 반환하는 단순 CRUD입니다.

*   **`GET /stores`**
    *   모든 매장 목록 조회. (`id`, `name`, `code`)
*   **`GET /categories`**
    *   모든 카테고리 목록 조회. `sort_order` 기준으로 정렬.

### Task 2: 관리자 리포트 서비스 구현 (`app/services/report.py` 또는 `inventory.py`)

*   **`get_low_stock_items(db: AsyncSession)`**
    *   `CurrentStock` 테이블에서 `quantity < product.safety_stock` 조건으로 필터링.
    *   `Product`, `Store` 정보를 Join해서 반환.
*   **`generate_low_stock_excel(items: List[StockItem]) -> BytesIO`**
    *   메모리 상에서 엑셀 파일 생성.
    *   헤더: [제품명, 바코드, 매장명, 현재고, 안전재고, 부족수량]
    *   데이터 행 추가.

### Task 3: 관리자 API 엔드포인트 구현 (`app/api/v1/admin.py` 또는 분산)

*   **`GET /alerts/low-stock`** (Admin Only)
    *   Dependency: `role="ADMIN"` 체크.
    *   위의 서비스 함수 호출하여 JSON 반환.
*   **`GET /exports/low-stock`** (Admin Only)
    *   위의 엑셀 생성 함수 호출.
    *   Response Class: `StreamingResponse` (FastAPI)
    *   Media Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
    *   Filename: `low_stock_{date}.xlsx`

---

## 3. 참고 자료

### 라이브러리
- `openpyxl`: 엑셀 파일 생성에 적합합니다. `requirements.txt`에 추가가 필요할 수 있습니다.

### 응답 예시 (Low Stock)
```json
[
  {
    "productName": "수분크림",
    "storeName": "강남점",
    "current": 5,
    "safety": 10,
    "shortage": 5
  }
]
```

---

## 4. 완료 조건 (Definition of Done)
1. `/stores`, `/categories` API가 정상 동작해야 함.
2. `/exports/low-stock` 호출 시 브라우저에서 엑셀 파일이 다운로드 되어야 하며, 내용이 DB와 일치해야 함.
3. 비관리자(WORKER)가 관리자 API 접근 시 403 Forbidden 에러 발생.
