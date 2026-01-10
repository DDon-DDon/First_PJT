# 구현 리포트: Phase 5 - 트랜잭션 (입출고) API

**작성일**: 2026-01-08
**구현 범위**: 재고 입고/출고/조정 트랜잭션 처리 및 이력 조회
**담당자**: Backend Agent (Claude)

---

## 1. 개요

Phase 5에서는 재고를 실제로 변경하는 **트랜잭션(Transaction)** 로직을 구현했습니다.
단순 데이터 생성을 넘어, 재고 수량의 **원자적 업데이트(Atomic Update)**와 **재고 부족 검증**, **안전재고 알림** 등 핵심 비즈니스 로직이 포함되었습니다.

### 주요 변경 사항 요약
- **API 엔드포인트**: `POST /inbound`, `POST /outbound`, `POST /adjust`, `GET /transactions`
- **비즈니스 로직**:
    - 입고: 재고 증가
    - 출고: 재고 검증 및 감소, 안전재고 알림 체크
    - 조정: 재고 정정 (증감 모두 가능), 사유 기록
- **데이터 무결성**: 트랜잭션 기록과 현재고(`CurrentStock`) 갱신을 하나의 DB 트랜잭션으로 처리

---

## 2. 상세 구현 내용

### 2.1 스키마 확장 (`app/schemas/transaction.py`)

트랜잭션 처리 결과를 클라이언트에게 즉시 피드백하기 위해 응답 스키마를 확장했습니다.
- `TransactionResultResponse` 추가:
    - `newStock`: 변경 후 현재고
    - `safetyAlert`: 안전재고 미만 여부 (True/False)

### 2.2 서비스 레이어 (`app/services/inventory.py`)

`InventoryService`를 확장하여 트랜잭션 처리 메서드를 추가했습니다.

- **`process_inbound`**:
    - `CurrentStock`이 없으면 생성(0) 후 증가시킵니다.
    - 양수 수량만 허용하며, 트랜잭션 타입은 `INBOUND`로 기록됩니다.
- **`process_outbound`**:
    - **재고 검증**: `CurrentStock.quantity < requested`일 경우 `InsufficientStockException`을 발생시킵니다.
    - **안전재고 체크**: 출고 후 잔여량이 안전재고 미만이면 `safety_alert=True`를 반환합니다.
- **`process_adjust`**:
    - 음수 조정 시 재고가 0 미만으로 떨어지는 것을 방지하는 최소한의 방어 로직을 추가했습니다.
    - `reason` (조정 사유) 필드를 필수로 처리합니다.
- **`list_transactions`**:
    - 매장, 제품, 타입별 필터링과 페이지네이션을 지원하는 이력 조회 기능을 구현했습니다.

### 2.3 API 라우터 (`app/api/v1/transactions.py`)

- **POST 메서드**: 입고, 출고, 조정 각각에 대한 전용 엔드포인트를 제공하여 명시적인 의도를 드러냅니다.
- **예외 처리**: 서비스 계층에서 발생하는 `InsufficientStockException`을 400 Bad Request로 처리합니다.
- **응답**: `TransactionResultResponse`를 사용하여 변경된 재고량과 경고 상태를 포함합니다.

### 2.4 테스트 코드 (`tests/test_transactions.py`)

비즈니스 로직의 정확성을 검증하는 6개의 테스트 케이스를 작성했습니다.

| 테스트 케이스 | 설명 | 결과 |
|--------------|------|------|
| `test_inbound_success` | 입고 성공 및 재고 증가 확인 | ✅ Pass |
| `test_inbound_accumulate` | 연속 입고 시 재고 누적 확인 | ✅ Pass |
| `test_outbound_success` | 출고 성공 및 재고 감소 확인 | ✅ Pass |
| `test_outbound_insufficient_stock` | 재고 부족 시 400 에러 확인 | ✅ Pass |
| `test_outbound_safety_alert` | 출고 후 안전재고 미만 알림 확인 | ✅ Pass |
| `test_adjust_stock` | 조정(폐기 등) 처리 및 사유 기록 확인 | ✅ Pass |

---

## 3. 기술적 이슈 및 해결

### 이슈 1: 모델 정의 오류 (`InventoryTransaction`)
- **증상**: 모델 로드 시 `TypeError` 발생.
- **원인**: `InventoryTransaction` 모델의 `relationship` 정의에 지원되지 않는 `comment` 인자가 포함됨.
- **해결**: `app/models/transaction.py`에서 `comment` 인자 제거.

### 이슈 2: 응답 스키마 매핑 (`TransactionResponse`)
- **증상**: API 응답 시 필드 누락 에러 (`userId` 등).
- **원인**: Pydantic 모델 필드명(camelCase)과 ORM 모델 속성명(snake_case) 불일치.
- **해결**: `alias`를 사용하여 명시적 매핑 적용 (`userId` -> `user_id`).

### 이슈 3: 지연 로딩 (Lazy Loading)
- **증상**: 안전재고 체크 시 `stock.product` 접근이 비동기 환경에서 실패할 가능성.
- **해결**: `_get_or_create_stock` 쿼리 시 `joinedload(CurrentStock.product)`를 사용하여 미리 로딩하거나, 없을 경우 `db.get(Product)`로 별도 조회하는 방어 로직 구현.

---

## 4. 커밋 메시지 (제안)

작업 내용을 바탕으로 한 단계별 커밋 메시지입니다.

```bash
# 1. 모델 수정
fix(models): remove invalid comment arg from transaction relationships

# 2. 스키마 확장
feat(schemas): add TransactionResultResponse and fix aliases

# 3. 서비스 구현
feat(services): implement inbound, outbound, and adjust transaction logic
feat(services): add insufficient stock validation and safety alert check

# 4. API 구현
feat(api): add transaction endpoints (inbound, outbound, adjust, list)

# 5. 설정
config(router): register transactions router in main app

# 6. 테스트
test(transactions): add integration tests for inventory transactions
```
