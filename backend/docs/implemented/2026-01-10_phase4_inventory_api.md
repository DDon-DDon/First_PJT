# 구현 리포트: Phase 4 - 재고 (Inventory) 조회 API

**작성일**: 2026-01-08
**구현 범위**: 현재고 조회, 상태 계산(LOW/NORMAL/GOOD), 권한별 필터링
**담당자**: Backend Agent (Claude)

---

## 1. 개요

Phase 4에서는 매장별 재고 현황을 조회하는 기능을 구현했습니다.
단순 수량 조회를 넘어, 안전재고 대비 상태(Status)를 동적으로 계산하여 제공하고, 사용자 역할(WORKER/ADMIN)에 따른 엄격한 데이터 접근 제어를 적용했습니다.

### 주요 변경 사항 요약
- **API 엔드포인트**:
    - `GET /inventory/stocks`: 조건별 재고 목록 조회 (WORKER는 본인 매장만)
    - `GET /inventory/stocks/{product_id}`: 제품별 전체 매장 재고 조회 (ADMIN 전용)
- **서비스 로직**:
    - `get_stock_status`: 수량과 안전재고를 비교하여 상태(LOW/NORMAL/GOOD) 판별
    - `get_current_stocks`: 권한 기반 쿼리 필터링 및 조인 최적화
- **데이터 모델 보완**:
    - `UserStore` 모델 및 `User-Store` N:M 관계 정의 추가 (Phase 1 누락분 보완)

---

## 2. 상세 구현 내용

### 2.1 데이터 모델 보완 (`app/models/user_store.py`)

WORKER의 매장 접근 권한을 제어하기 위해 `User`와 `Store` 간의 다대다 관계를 정의했습니다.
- `UserStore` 모델 생성 (Association Table)
- `User.stores` 및 `Store.users` 관계 설정 (`selectin` 로딩 전략 사용)

### 2.2 서비스 레이어 (`app/services/inventory.py`)

- **권한 제어 로직**:
    - `WORKER`: `UserStore` 테이블을 조회하여 배정된 매장 ID 목록(`allowed_store_ids`)을 확보하고, 이를 기반으로 `CurrentStock` 쿼리를 강제 필터링했습니다.
    - `ADMIN`: 모든 매장에 접근 가능하며, `store_id` 파라미터로 특정 매장을 조회할 수 있습니다.
- **상태 계산 로직**:
    - `LOW`: 현재고 < 안전재고
    - `NORMAL`: 안전재고 <= 현재고 < 안전재고 * 2
    - `GOOD`: 현재고 >= 안전재고 * 2
    - API 응답 시 이 로직을 적용하여 클라이언트에 `status` 필드를 제공합니다.

### 2.3 API 라우터 (`app/api/v1/inventory.py`)

- **응답 변환**:
    - 서비스 계층에서 반환된 `CurrentStock` ORM 객체를 순회하며 `status`를 계산하고 `StockItemResponse` Pydantic 모델로 변환했습니다.
- **상태 필터링 (`status` Query Param)**:
    - DB 레벨에서 수량 조건을 적용하여 `LOW`, `NORMAL`, `GOOD` 상태인 재고만 필터링하여 조회하는 기능을 구현했습니다.

### 2.4 테스트 코드 (`tests/test_inventory.py`)

- **Unit Test**: 상태 계산 로직(`get_stock_status`) 검증
- **Integration Test**:
    - `test_list_stocks_worker`: 작업자가 본인 매장 재고만 조회하는지 확인
    - `test_list_stocks_admin`: 관리자가 특정 매장 재고를 조회하는지 확인
    - `test_list_stocks_status_filter`: 상태값 필터링 동작 확인
    - `test_get_product_stock_detail`: 제품별 상세 재고 조회 확인

---

## 3. 기술적 이슈 및 해결

### 이슈 1: Phase 1 모델 누락 (`UserStore`)
- **증상**: `User.stores` 관계에 접근할 수 없어 작업자 권한 체크 구현 불가.
- **원인**: Phase 1에서 N:M 관계 테이블 정의가 누락됨.
- **해결**: `app/models/user_store.py` 생성 및 `User`, `Store` 모델에 `relationship` 추가.

### 이슈 2: 테스트 데이터 제약 조건 (`password_hash`)
- **증상**: `User` 생성 시 `IntegrityError: NOT NULL constraint failed: users.password_hash` 발생.
- **원인**: 테스트 코드에서 필수 필드인 `password_hash`를 누락함.
- **해결**: 테스트 픽스처 생성 시 더미 해시값 추가.

### 이슈 3: SQLAlchemy Async Lazy Loading
- **증상**: 비동기 세션에서 `user.stores` 접근 시 `MissingGreenlet` 에러 가능성.
- **해결**: `get_current_stocks` 함수 내에서 `UserStore` 테이블을 직접 쿼리(`select(UserStore.store_id)...`)하여 명시적으로 권한을 확인하는 방식으로 구현. (안전성 확보)

---

## 4. 향후 계획

- **Phase 5 (트랜잭션 API)**: 재고를 실제로 변경(입고/출고)하는 트랜잭션 처리 구현.
- **동시성 제어**: 입출고 시 재고 데이터 정합성을 위한 Locking 전략 적용 필요.
