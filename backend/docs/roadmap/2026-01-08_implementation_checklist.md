# 똔똔(DoneDone) 상세 구현 로드맵 체크리스트

**작성일**: 2026-01-08
**기반 문서**:
- [개발 상태 리포트](./2026-01-08_development-status.md)
- [PRD](../../../.claude/skills/ddon-project/references/prd.md)
- [API 명세서](../../../.claude/skills/ddon-project/references/api-spec.md)
- [ERD](../../../.claude/skills/ddon-project/references/erd.md)

---

## ✅ Phase 1: 데이터베이스 & 스키마 (완료)

- [x] **모델 구현** (`app/models/`)
    - [x] `User` 모델 (WORKER/ADMIN role)
    - [x] `Store` 모델
    - [x] `Category` 모델
    - [x] `Product` 모델 (barcode unique index)
    - [x] `CurrentStock` 모델 (Composite PK: product_id + store_id)
    - [x] `InventoryTransaction` 모델 (Append-only)
- [x] **Pydantic 스키마 구현** (`app/schemas/`)
    - [x] User schemas (Create, Update, Response)
    - [x] Product schemas
    - [x] Transaction schemas
    - [x] Common schemas (Pagination, Response)
- [x] **인프라 설정**
    - [x] PostgreSQL Async Engine 설정
    - [x] Alembic 마이그레이션 환경
    - [x] Pytest 픽스처 (`conftest.py`)

---

## 🚀 Phase 2: 인증 (Auth) API (후순위 - 나중에 작업)

### 2.1 테스트 작성 (TDD)
- [ ] `tests/test_auth.py` 생성
    - [ ] `test_login_success`: 올바른 이메일/비번으로 토큰 수신 확인
    - [ ] `test_login_invalid_password`: 잘못된 비번 시 401 에러
    - [ ] `test_login_user_not_found`: 존재하지 않는 이메일 시 401/404 에러
    - [ ] `test_refresh_token`: Refresh 토큰으로 새 Access 토큰 발급
    - [ ] `test_get_current_user`: 유효한 토큰으로 내 정보 조회

### 2.2 서비스 레이어 구현 (`app/services/auth.py`)
- [ ] `authenticate_user(email, password)`: DB 조회 및 비번 검증
- [ ] `create_access_token(data)`: JWT Access Token 생성 (60분)
- [ ] `create_refresh_token(data)`: JWT Refresh Token 생성 (7일)
- [ ] `get_current_user(token)`: 토큰 디코딩 및 사용자 DB 조회

### 2.3 API 엔드포인트 구현 (`app/api/v1/auth.py`)
- [ ] **POST /auth/login**
    - [ ] Request Body 검증 (`UserLogin`)
    - [ ] Service 호출 및 토큰 생성
    - [ ] Response 반환 (accessToken, refreshToken, user info)
- [ ] **POST /auth/refresh**
    - [ ] Refresh Token 검증
    - [ ] 새 Access Token 발급
- [ ] **GET /auth/me**
    - [ ] `Depends(get_current_user)` 의존성 주입 확인
    - [ ] 사용자 정보 반환

---

## 📦 Phase 3: 제품 (Product) API (완료)

### 3.1 테스트 작성
- [x] `tests/test_products.py` 생성
    - [x] `test_get_product_by_barcode`: 바코드 조회 성공/실패
    - [x] `test_list_products`: 페이지네이션 및 필터 동작 확인
    - [x] `test_create_product_admin`: 관리자 권한으로 제품 생성
    - [x] `test_create_product_worker_fail`: 작업자 권한으로 생성 시도 시 403

### 3.2 서비스 레이어 구현 (`app/services/product.py`)
- [x] `get_product_by_barcode(barcode)`: 바코드 인덱스 활용 조회 (성능 중요)
- [x] `list_products(params)`: 검색(이름/바코드), 카테고리 필터, 페이지네이션
- [x] `create_product(data)`: 바코드 중복 체크 후 생성

### 3.3 API 엔드포인트 구현 (`app/api/v1/products.py`)
- [x] **GET /products/barcode/{barcode}** (⚡ < 1초 목표)
    - [x] 존재 시 200 OK + 제품 정보
    - [x] 미존재 시 404 Not Found
- [x] **GET /products**
    - [x] Query Params: `page`, `limit`, `search`, `category_id`
    - [x] 리스트 응답 구현
- [x] **POST /products** (ADMIN Only)
    - [x] 관리자 권한 체크 (`current_user.role == 'ADMIN'`)
    - [x] 제품 생성 및 201 Created

---

## 🏭 Phase 4: 재고 (Inventory) 조회 API (완료)

### 4.1 테스트 작성
- [x] `tests/test_inventory.py` (조회 관련)
    - [x] `test_get_stock_status`: 재고 수량에 따른 상태(LOW/NORMAL/GOOD) 확인
    - [x] `test_get_stocks_list`: 매장별/카테고리별 재고 목록 조회

### 4.2 서비스 레이어 구현 (`app/services/inventory.py`)
- [x] `get_stock_status(quantity, safety_stock)`: 상태 결정 로직 구현
- [x] `get_current_stocks(store_id, params)`: `CurrentStock` 테이블 조인 조회

### 4.3 API 엔드포인트 구현 (`app/api/v1/inventory.py`)
- [x] **GET /inventory/stocks**
    - [x] WORKER: 본인 배정 매장 강제 필터링
    - [x] ADMIN: `store_id` 파라미터로 선택 가능
    - [x] Response에 `status` 필드 계산 포함
- [x] **GET /inventory/stocks/{productId}**
    - [x] 해당 제품의 모든 매장 재고 현황 조회 (ADMIN용)

---

## 🚚 Phase 5: 트랜잭션 (입출고) API (완료)

### 5.1 테스트 작성 (핵심 비즈니스 로직)
- [x] `tests/test_transactions.py` 생성
    - [x] `test_inbound`: 재고 증가 및 트랜잭션 기록 확인
    - [x] `test_outbound_success`: 재고 감소 및 트랜잭션 기록 확인
    - [x] `test_outbound_insufficient`: 재고 부족 시 400 에러 확인
    - [x] `test_outbound_safety_alert`: 안전재고 미만 도달 시 알림 플래그 확인
    - [x] `test_adjust_stock`: 조정(폐기 등) 처리 확인

### 5.2 서비스 레이어 구현 (`app/services/inventory.py` 확장)
- [x] `process_inbound(data)`:
    - [x] Transaction INSERT (type=INBOUND)
    - [x] CurrentStock UPDATE (quantity += input) (Upsert 로직 필요)
- [x] `process_outbound(data)`:
    - [x] CurrentStock Lock (for update) 또는 원자적 연산
    - [x] 재고 부족 체크 (`current < request` -> Error)
    - [x] Transaction INSERT (type=OUTBOUND)
    - [x] CurrentStock UPDATE (quantity -= input)
    - [x] 안전재고 체크 로직
- [x] `process_adjust(data)`:
    - [x] Transaction INSERT (type=ADJUST, reason 필수)
    - [x] CurrentStock UPDATE

### 5.3 API 엔드포인트 구현 (`app/api/v1/transactions.py`)
- [x] **POST /transactions/inbound**
- [x] **POST /transactions/outbound**
    - [x] 예외 처리: `InsufficientStockError` -> 400 Bad Request 변환
- [x] **POST /transactions/adjust**
- [x] **GET /transactions**
    - [x] 필터: `store_id`, `product_id`, `type`, `date_range`

---

## 🔄 Phase 6: 동기화 (Sync) API (완료)

### 6.1 테스트 작성
- [x] `tests/test_sync.py`
    - [x] `test_sync_batch`: 여러 트랜잭션 일괄 처리 확인
    - [x] `test_sync_duplicate`: 이미 동기화된 트랜잭션(localId 중복) 무시 확인

### 6.2 서비스 레이어 구현 (`app/services/sync.py`)
- [x] `sync_transactions(transactions_list)`:
    - [x] Loop 처리 또는 Bulk Insert 최적화
    - [x] `local_id` 중복 체크 (Idempotency)
    - [x] 각 트랜잭션 처리 후 결과(성공/실패) 집계

### 6.3 API 엔드포인트 구현 (`app/api/v1/sync.py`)
- [x] **POST /sync/transactions**
    - [x] Request: 오프라인에서 생성된 트랜잭션 배열
    - [x] Response: 성공한 localId 목록, 실패한 목록

---

## 🏪 Phase 7: 매장/카테고리 및 관리자 API (완료)

### 7.1 구현 목록
- [x] `app/api/v1/stores.py`: **GET /stores** (매장 목록)
- [x] `app/api/v1/categories.py`: **GET /categories** (카테고리 목록)
- [x] **GET /alerts/low-stock** (ADMIN)
    - [x] `CurrentStock` 중 `quantity < product.safety_stock` 인 항목 조회
- [x] **GET /exports/low-stock** (ADMIN)
    - [x] `pandas` 또는 `openpyxl` 등을 사용하여 Excel 파일 생성 및 반환

---

## 🧪 Phase 8: E2E 통합 테스트

### 8.1 시나리오 테스트 (`tests/test_e2e.py`)
- [ ] **전체 워크플로우 검증**
    1. 관리자 로그인 & 제품 등록
    2. 작업자 로그인
    3. 입고 처리 (재고 0 -> 30)
    4. 현재고 조회 확인 (30)
    5. 출고 처리 (30 -> 20)
    6. 재고 부족 출고 시도 (20 -> -10 요청) -> 실패 확인
    7. 트랜잭션 이력 조회

---

## 🛠 공통/기타 작업
- [ ] **에러 핸들링**: 전역 예외 처리기 (`app/main.py`) 등록
- [ ] **CORS 설정**: 프론트엔드 연동 대비
- [ ] **Logging**: 주요 액션에 대한 로깅 추가
- [ ] **Docker**: `Dockerfile` 및 `docker-compose.yml` 최종 점검
