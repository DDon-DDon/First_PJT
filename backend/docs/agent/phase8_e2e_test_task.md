# 개발 지시서: Phase 8 - E2E 통합 테스트 작성

**작성일**: 2026-01-08
**대상 에이전트**: Backend Developer Agent
**목표**: 시스템의 전체 워크플로우(제품 등록부터 입고, 출고, 이력 확인까지)가 유기적으로 동작하는지 검증하는 E2E 테스트를 작성한다.

---

## 1. 개요 및 컨텍스트

단위 테스트(Unit Test)는 개별 모듈을 검증하지만, 모듈 간의 연결 고리는 검증하지 못합니다.
**Phase 8**에서는 실제 API 클라이언트(`AsyncClient`)를 사용하여 사용자 시나리오를 처음부터 끝까지 수행하는 통합 테스트 코드를 작성합니다.

**중요 요구사항**:
- **상태 유지**: 하나의 시나리오 안에서 데이터 상태가 유지되어야 합니다. (예: 입고 후 재고 조회 시 수량이 변경되어 있어야 함)
- **현실적인 시나리오**: 실제 사용자가 앱을 사용하는 순서대로 API를 호출해야 합니다.

---

## 2. 작업 상세 내용

### Task 1: 테스트 시나리오 구현 (`tests/test_e2e.py`)

다음 순서대로 동작하는 `test_complete_inventory_workflow` 함수를 작성하세요.

1.  **관리자 로그인 & 준비**
    *   (Auth가 Mocking된 경우 헤더 조작)
    *   `POST /products`: 테스트용 신규 제품("E2E 테스트용 크림") 등록.
    *   `barcode` 저장.
2.  **초기 상태 확인**
    *   `GET /products/barcode/{barcode}`: 제품 조회 성공 확인.
    *   `GET /inventory/stocks/{product_id}`: 초기 재고 0 또는 데이터 없음 확인.
3.  **입고 (Inbound)**
    *   `POST /transactions/inbound`: 수량 50개 입고.
    *   Response에서 `newStock: 50` 확인.
4.  **중간 상태 확인**
    *   `GET /inventory/stocks`: 재고 목록에 해당 제품이 50개로 조회되는지, 상태가 `GOOD`인지 확인.
5.  **출고 (Outbound)**
    *   `POST /transactions/outbound`: 수량 45개 출고.
    *   Response에서 `newStock: 5` 확인. `safetyAlert: true` (안전재고가 10이라면) 확인.
6.  **재고 부족 출고 시도**
    *   `POST /transactions/outbound`: 수량 10개 출고 시도.
    *   **400 Error** 발생 확인.
7.  **트랜잭션 이력 확인**
    *   `GET /transactions`: 위에서 수행한 입고(1건), 출고(1건) 내역이 조회되는지 확인.

### Task 2: 버그 수정 및 안정화
E2E 테스트를 돌리면서 발견되는 버그(예: 트랜잭션 커밋 문제, 데이터 조회 시점 문제 등)를 수정합니다.

---

## 3. 참고 자료

### Pytest Fixture
`conftest.py`에 정의된 `client`와 `db_session`을 적극 활용하세요. 데이터베이스는 테스트 시작 시점에 초기화(Reset) 되거나, 테스트용 격리 DB를 사용해야 합니다.

---

## 4. 완료 조건 (Definition of Done)
1. `pytest tests/test_e2e.py` 명령어가 에러 없이 통과해야 함.
2. 테스트 수행 후 DB에 불필요한 더미 데이터가 남지 않도록 정리(Teardown)되거나, 인메모리 DB를 사용하여 자연스럽게 소멸되어야 함.
