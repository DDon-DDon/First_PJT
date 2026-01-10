# 구현 리포트: Phase 6 - 동기화 (Sync) API

**작성일**: 2026-01-08
**구현 범위**: 오프라인 트랜잭션 일괄 동기화 (Batch Sync)
**담당자**: Backend Agent (Claude)

---

## 1. 개요

Phase 6에서는 네트워크 연결이 끊긴 상태(오프라인)에서 클라이언트가 생성한 트랜잭션을 서버로 일괄 전송하고 동기화하는 기능을 구현했습니다.
**멱등성(Idempotency)** 보장과 **부분 성공(Partial Success)** 처리가 핵심 요구사항이었습니다.

### 주요 변경 사항 요약
- **데이터 모델**: `InventoryTransaction`에 `local_id` (UUID, Unique) 컬럼 추가
- **API 엔드포인트**: `POST /sync/transactions` (배치 처리)
- **서비스 로직**:
    - `local_id` 중복 체크로 이미 처리된 트랜잭션 Skip
    - 개별 트랜잭션 처리 중 오류 발생 시 해당 건만 실패 처리하고 나머지는 진행
    - `synced_at` 타임스탬프 기록

---

## 2. 상세 구현 내용

### 2.1 데이터 모델 수정 (`app/models/transaction.py`)

클라이언트에서 생성한 고유 ID를 저장하기 위해 `local_id` 컬럼을 추가했습니다.
```python
local_id = Column(GUID, nullable=True, unique=True, comment="클라이언트 로컬 ID")
```
이 컬럼은 Unique 제약조건을 가지며, 동일한 요청이 중복 전송되더라도 서버에서 중복 처리를 방지하는 키 역할을 합니다.

### 2.2 스키마 정의 (`app/schemas/sync.py`)

배치 요청 및 응답을 위한 전용 스키마를 정의했습니다.
- `SyncRequest`: 트랜잭션 아이템 리스트
- `SyncResponse`: 성공 목록(`synced`)과 실패 목록(`failed`)을 분리하여 반환

### 2.3 서비스 레이어 (`app/services/sync.py`)

`sync_transactions` 함수는 다음 순서로 동작합니다.
1. 요청된 트랜잭션 리스트를 순회합니다.
2. **중복 체크**: DB에서 `local_id` 조회. 이미 존재하면 `synced` 리스트에 추가하고 Skip (Idempotency).
3. **트랜잭션 처리**:
    - `inventory_service`의 `process_inbound/outbound/adjust` 함수를 재사용하여 로직 일관성 유지.
    - 트랜잭션 생성 후 `local_id`와 `synced_at`을 업데이트.
4. **예외 처리**:
    - 개별 트랜잭션 처리 중 에러(예: 재고 부족) 발생 시 `rollback` 후 `failed` 리스트에 에러 메시지와 함께 추가.
    - 전체 프로세스가 멈추지 않고 다음 트랜잭션으로 진행.

### 2.4 테스트 코드 (`tests/test_sync.py`)

- **`test_sync_batch_success`**: 여러 건의 정상 트랜잭션이 모두 DB에 저장되는지 확인.
- **`test_sync_duplicate_ignore`**: 동일한 `local_id` 요청을 두 번 보내도 데이터가 중복 생성되지 않는지 확인.
- **`test_sync_partial_fail`**: 3건 중 1건이 실패(재고 부족)하더라도 나머지 2건은 정상 저장되는지 확인.

---

## 3. 기술적 이슈 및 해결

### 이슈 1: 비동기 세션 롤백 후 객체 접근 오류 (`MissingGreenlet`)
- **증상**: 테스트 코드(`test_sync_partial_fail`)에서 트랜잭션 실패로 `rollback()`이 호출된 후, 다음 트랜잭션 처리 시 `MissingGreenlet: greenlet_spawn has not been called...` 에러 발생.
- **원인**: 테스트 Fixture에서 생성하여 세션에 포함된 `user` 객체가 `rollback`으로 인해 만료(Expire)됨. 이후 코드에서 `user.id`에 접근할 때 비동기 환경에서 암시적 I/O(Refresh)가 발생하여 에러 유발.
- **해결**: 테스트 코드에서 `app.dependency_overrides`에 `user` 객체를 주입하기 전에 `db_session.expunge(user)`를 호출하여 세션에서 분리(Detach)함. 이를 통해 `rollback`의 영향을 받지 않는 순수 객체 상태로 유지.

### 이슈 2: 스키마 필드 매핑
- **증상**: `local_id` 등 snake_case 필드가 API 요청/응답의 camelCase와 매핑되지 않음.
- **해결**: Pydantic 스키마에서 `alias="localId"` 및 `populate_by_name=True` 설정을 통해 양방향 매핑 지원.

---

## 4. 커밋 메시지 (제안)

```bash
Feat: Implement Offline Sync API (Phase 6)

- Add `local_id` column to `InventoryTransaction` for idempotency
- Implement `POST /sync/transactions` endpoint for batch processing
- Add `SyncService` with duplicate check and partial success logic
- Add `SyncRequest` and `SyncResponse` schemas
- Add integration tests for batch sync, duplicate ignore, and partial failure handling
- Fix: Detach user object in tests to prevent MissingGreenlet error on rollback
```
