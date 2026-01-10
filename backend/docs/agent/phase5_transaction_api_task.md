# 개발 지시서: Phase 5 - 트랜잭션 (입출고) API 구현

**작성일**: 2026-01-08
**대상 에이전트**: Backend Developer Agent
**목표**: 재고의 입고, 출고, 조정을 처리하는 핵심 비즈니스 로직을 구현한다.

---

## 1. 개요 및 컨텍스트

**Phase 5**는 시스템의 핵심인 재고 변경(트랜잭션)을 다룹니다.
단순히 숫자를 바꾸는 것이 아니라, `InventoryTransaction`에 이력을 남기고(Append-Only), `CurrentStock`을 갱신하는 과정이 원자적(Atomic)으로 이루어져야 합니다.

**중요 요구사항**:
- **데이터 무결성**: 트랜잭션 기록과 재고 갱신은 반드시 하나의 DB 트랜잭션 내에서 수행되어야 합니다.
- **재고 검증**: 출고(`OUTBOUND`) 시 현재고보다 많은 양을 요청하면 **400 에러**를 리턴해야 합니다.
- **안전재고 알림**: 출고 후 재고가 안전재고 미만으로 떨어지면, 응답의 `safetyAlert: true` 플래그를 설정합니다.

---

## 2. 작업 상세 내용

### Task 1: 단위 테스트 작성 (`tests/test_transactions.py`)
핵심 로직이므로 꼼꼼한 테스트 케이스가 필요합니다.

1.  **입고(Inbound) 테스트**
    *   `test_inbound_success`: 재고가 0에서 30으로 증가 확인, Transaction 레코드 생성 확인.
    *   `test_inbound_accumulate`: 기존 재고 10 + 입고 20 = 30 확인.
2.  **출고(Outbound) 테스트**
    *   `test_outbound_success`: 재고 감소 확인.
    *   `test_outbound_insufficient_stock`: 재고 부족 시 `HTTPException` 발생 확인.
    *   `test_outbound_safety_alert`: 안전재고 미만 도달 시 알림 트리거 확인.
3.  **조정(Adjust) 테스트**
    *   `test_adjust_stock`: `reason`(폐기 등)과 함께 재고 감소 확인.

### Task 2: 서비스 레이어 구현 (`app/services/inventory.py` 확장)
기존 Inventory 서비스에 트랜잭션 처리 메서드를 추가합니다.

*   **`process_inbound(db: AsyncSession, data: TransactionCreate, user: User)`**
    *   1. `CurrentStock` 조회 (없으면 생성).
    *   2. `InventoryTransaction` 생성 (type=`INBOUND`, quantity=`+N`).
    *   3. `CurrentStock.quantity` 증가.
*   **`process_outbound(db: AsyncSession, data: TransactionCreate, user: User)`**
    *   1. `CurrentStock` 조회 (Locking 고려: `with_for_update()`).
    *   2. 재고 부족 체크 (`current < request`). 부족 시 예외 발생.
    *   3. `InventoryTransaction` 생성 (type=`OUTBOUND`, quantity=`-N`).
    *   4. `CurrentStock.quantity` 감소.
    *   5. `safety_alert` 여부 판단 후 리턴 값에 포함.
*   **`process_adjust(db: AsyncSession, data: AdjustTransactionCreate, user: User)`**
    *   1. `InventoryTransaction` 생성 (type=`ADJUST`, reason 필수).
    *   2. `CurrentStock` 갱신 (증감 모두 가능).

### Task 3: API 엔드포인트 구현 (`app/api/v1/transactions.py`)
각 액션별 엔드포인트를 구현합니다.

*   **`POST /transactions/inbound`**
*   **`POST /transactions/outbound`**
    *   에러 핸들링: 서비스에서 발생한 `InsufficientStockError`를 잡아 400 Bad Request로 변환.
*   **`POST /transactions/adjust`**
*   **`GET /transactions`**
    *   이력 조회. 필터(`store_id`, `product_id`, `type`, 날짜 범위) 적용.

---

## 3. 참고 자료

### 트랜잭션 모델 (`models/transaction.py`)
```python
class TransactionType(str, Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    ADJUST = "ADJUST"
```

### 동시성 처리
FastAPI + SQLAlchemy AsyncSession 환경이므로, `await session.refresh(stock, with_for_update=True)` 등을 활용하여 Race Condition을 방지하는 것이 좋습니다.

---

## 4. 완료 조건 (Definition of Done)
1. 모든 테스트 케이스(`tests/test_transactions.py`) 통과.
2. 출고 시 재고 부족 에러가 정확히 발생해야 함.
3. 모든 재고 변경 사항이 `InventoryTransaction` 테이블에 누락 없이 기록되어야 함.
