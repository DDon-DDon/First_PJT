# 개발 지시서: Phase 6 - 동기화 (Sync) API 구현

**작성일**: 2026-01-08
**대상 에이전트**: Backend Developer Agent
**목표**: 오프라인 상태에서 발생한 트랜잭션을 서버로 일괄 동기화하는 기능을 구현한다.

---

## 1. 개요 및 컨텍스트

클라이언트(앱/웹)가 네트워크 연결이 없는 상태에서도 입출고 작업을 수행한 뒤, 네트워크가 복구되었을 때 이 데이터들을 한꺼번에 서버로 전송합니다.
**Phase 6**는 이 '배치 동기화' 요청을 받아 처리하는 API입니다.

**중요 요구사항**:
- **멱등성 (Idempotency)**: 클라이언트가 실수로 같은 데이터를 두 번 보내더라도, 서버에는 한 번만 기록되어야 합니다. (`local_id` 활용)
- **일괄 처리 (Batch Processing)**: 수십 건의 트랜잭션이 한 번의 요청으로 들어올 수 있습니다. 성능을 고려해야 합니다.
- **부분 성공 허용**: 일부 트랜잭션이 실패하더라도(예: 재고 부족), 나머지는 성공 처리하고 실패 목록을 응답으로 알려주어야 합니다.

---

## 2. 작업 상세 내용

### Task 1: 단위 테스트 작성 (`tests/test_sync.py`)

1.  **배치 동기화 성공 테스트**
    *   `test_sync_batch_success`: 여러 개의 정상 트랜잭션을 보냈을 때 모두 DB에 저장되는지 확인.
2.  **중복 방지 테스트**
    *   `test_sync_duplicate_ignore`: 이미 저장된 `local_id`를 가진 트랜잭션이 다시 오면 무시(Skip)하고 성공으로 간주하는지 확인.
3.  **부분 실패 테스트** (고급)
    *   `test_sync_partial_fail`: 3개 중 1개가 재고 부족으로 실패할 때, 나머지 2개는 저장되고 응답에 실패 1건이 명시되는지 확인.

### Task 2: 서비스 레이어 구현 (`app/services/sync.py`)

*   **`sync_transactions(db: AsyncSession, transactions: List[SyncTransactionSchema], user: User)`**
    *   입력받은 트랜잭션 리스트를 순회합니다.
    *   각 트랜잭션에 대해:
        1. `InventoryTransaction` 테이블에서 `local_id` (클라이언트 생성 UUID) 중복 체크.
            - 중복이면: 결과 리스트에 '성공(Skip)'으로 추가하고 `synced_at` 갱신.
        2. 중복이 아니면: 해당 트랜잭션 타입(IN/OUT/ADJUST)에 맞는 `inventory_service` 로직 호출.
            - 성공 시: `InventoryTransaction`에 `local_id`, `synced_at` 저장.
            - 실패 시: 에러 메시지와 함께 실패 리스트에 추가.
    *   최종적으로 `{ synced: [...], failed: [...] }` 구조 반환.

### Task 3: API 엔드포인트 구현 (`app/api/v1/sync.py`)

*   **`POST /sync/transactions`**
    *   Request Body: `SyncRequest` (트랜잭션 배열)
    *   Response Model: `SyncResponse`
        *   `synced`: 동기화 완료된 `local_id`와 서버에서 발급한 `id` 매핑 리스트.
        *   `failed`: 실패한 `local_id`와 에러 메시지 리스트.

---

## 3. 참고 자료

### 스키마 예시
```python
class SyncTransactionItem(BaseModel):
    local_id: UUID
    type: TransactionType
    product_id: UUID
    store_id: UUID
    quantity: int
    created_at: datetime
    # ...
```

### 전략
- `InventoryTransaction` 모델에 `local_id` 컬럼이 있는지 확인 필요 (없으면 JSON 필드나 별도 컬럼으로 관리 고려. 현재 ERD에는 명시 안되어 있을 수 있으니 `note`에 넣거나 컬럼 추가 필요. **Note**: ERD에 `local_id`가 없다면 `note` 필드에 JSON 형태로 저장하거나, 마이그레이션으로 컬럼 추가를 고려하세요. 이번 지시서에서는 **컬럼 추가**를 권장합니다.)

---

## 4. 완료 조건 (Definition of Done)
1. `tests/test_sync.py` 통과.
2. 동일한 Payload를 두 번 보내도 데이터가 중복해서 쌓이지 않아야 함.
3. 오프라인에서 생성된 `created_at` 시간이 서버 DB에도 그대로 유지되어야 함.
