# Phase D: 쿼리 최적화 & 벤치마크 구현 문서

**작성일**: 2026-01-31  
**작성자**: Antigravity Project Team  
**Phase 기간**: 2026-01-31 ~ 2026-01-31  
**관련 커밋**: feat(db): optimize query performance (Phase D completed)

---

## 1. 개요 (Overview)

### 1.1 목적

- 대규모 재고 데이터 처리 시 발생할 수 있는 데이터베이스 성능 저하 방지
- N+1 문제 조기 발견 및 해결을 통한 응답 속도 안정화
- 인덱스 최적화를 통한 주요 쿼리 조회 성능 향상
- 성능 기준선(Baseline) 측정을 위한 부하 테스트 환경 구축

### 1.2 범위

- **D-1**: 쿼리 분석 유틸리티 (`QueryCounter`, `explain_analyze`) 구현
- **D-2**: 주요 서비스(Inventory) N+1 문제 분석 및 해결 검증 (통합 테스트)
- **D-3**: `inventory_transactions` 등 대량 데이터 테이블 인덱스 최적화
- **D-4**: DB Connection Pool 설정 튜닝
- **D-5**: Locust 기반 부하 테스트 스크립트 작성

### 1.3 사전 조건

- Phase A, B, C 완료 (API, 테스트, 로깅 구축 완료)
- PostgreSQL 데이터베이스 (Asyncpg 비동기 드라이버)

---

## 2. 구현 내용 (Implementation Details)

### 2.1 아키텍처 개요

기존 비즈니스 로직(Service Layer)에 ORM 최적화(`joinedload`, `selectinload`)를 적용하고, DB 레이어(Alembic, Settings)에서 인덱스와 커넥션 풀을 관리하는 구조입니다. `QueryCounter`는 테스트 환경에서 쿼리 실행 횟수를 가로채 검증하는 역할을 합니다.

### 2.2 태스크별 구현

#### [D-1] 쿼리 분석 환경 구축

**파일**: `app/core/query_analyzer.py`

**핵심 코드**:

```python
class QueryCounter:
    """컨텍스트 내에서 실행된 쿼리 개수를 세는 컨텍스트 매니저"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.count = 0

    def __enter__(self):
        event.listen(self.session.sync_session.bind, "after_cursor_execute", self.callback)
        return self

    def callback(self, conn, cursor, statement, parameters, context, executemany):
        self.count += 1
```

**설명**: SQLAlchemy의 `after_cursor_execute` 이벤트를 활용하여 특정 코드 블록 내에서 발생한 실제 SQL 쿼리 횟수를 측정합니다. 이를 통해 N+1 문제를 검증합니다.

#### [D-2] N+1 문제 점검 및 해결

**파일**: `tests/integration/test_nplusone.py`

**핵심 코드**:

```python
async with QueryCounter(db_session) as counter:
    items, total = await get_current_stocks(db_session, store_id=store.id, ...)

# 데이터 개수가 늘어도 쿼리 수는 일정해야 함 (예: <= 3)
assert counter.count <= 3
```

**설명**: `app/services/product.py`와 `inventory.py`에서 `joinedload`를 사용하도록 확인/조치하였고, 통합 테스트를 통해 데이터가 5개일 때와 10개일 때 쿼리 수가 폭증하지 않음을 검증했습니다.

#### [D-3] 인덱스 최적화

**파일**: `app/models/transaction.py`, `alembic/versions/2b423957f08f_...py`

**핵심 코드**:

```python
# Model
class InventoryTransaction(Base):
    __table_args__ = (
        Index('idx_transactions_store_created', 'store_id', 'created_at'),
        Index('idx_transactions_product_created', 'product_id', 'created_at'),
    )

# Migration
def upgrade():
    op.create_index('idx_transactions_store_created', 'inventory_transactions', ['store_id', 'created_at'], unique=False)
```

**설명**: 재고 이력 조회 시 가장 빈번한 패턴인 "특정 매장의 기간별 조회", "특정 상품의 이력 조회"를 최적화하기 위해 복합 인덱스를 추가했습니다. 또한 Enum 타입의 `name`을 명시하여 Alembic의 불필요한 변경 감지를 방지했습니다.

#### [D-4] Connection Pool 튜닝

**파일**: `app/core/config.py`, `app/db/session.py`

**설명**: `.env` 파일에서 `DB_POOL_SIZE`와 `DB_MAX_OVERFLOW`를 설정할 수 있도록 `Settings` 클래스를 업데이트하고, `AsyncEngine` 생성 시 이를 반영했습니다.

#### [D-5] 벤치마크 및 성능 기준선

**파일**: `tests/load/locustfile.py`

**핵심 코드**:

```python
class InventoryUser(HttpUser):
    @task(3)
    def get_stocks(self):
        self.client.get("/api/v1/inventory/stocks?page=1&limit=10")
```

**설명**: Python 기반 부하 도구인 Locust를 사용하여 핵심 API의 성능을 측정할 수 있는 스크립트를 작성했습니다.

---

## 3. 설계 결정 (Design Decisions)

### 3.1 선택한 접근 방식

| 결정 사항   | 선택                        | 대안                | 선택 이유                                                                         |
| ----------- | --------------------------- | ------------------- | --------------------------------------------------------------------------------- |
| 쿼리 검증   | `event.listen` 기반 Counter | SQL Log 파싱        | 구현이 간단하고 테스트 코드 내에서 즉시 assert 가능                               |
| 인덱스 전략 | 복합 인덱스 (Composite)     | 단일 인덱스 여러 개 | `store_id`와 `created_at`은 거의 항상 함께 조건절에 사용됨 (Index Only Scan 유도) |
| Enum 처리   | Native Enum (DB)            | VARCHAR + Check     | 데이터 무결성 보장 및 저장 공간 효율성, `name` 명시로 마이그레이션 안정성 확보    |

### 3.2 트레이드오프 분석

**장점**:

- **성능 예측성**: 쿼리 카운터를 통한 정량적 검증 가능.
- **읽기 성능**: 주요 조회 쿼리의 속도 대폭 향상 예상.

**단점**:

- **쓰기 성능**: 인덱스 추가로 인한 쓰기 오버헤드 (미미한 수준으로 판단).
- **복잡성**: SQLAlchemy의 Eager Loading 전략(`joinedload` vs `selectinload`)을 신경 써야 함.

---

## 4. 사용 방법 (Usage Guide)

### 4.1 N+1 테스트 실행

```bash
pytest tests/integration/test_nplusone.py -v
```

### 4.2 부하 테스트 실행

```bash
# locust 설치 필요 (pip install locust)
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

브라우저에서 `http://localhost:8089` 접속하여 테스트 시작.

---

## 5. 테스트 및 검증 (Testing & Validation)

### 5.1 테스트 범위

- 단위 테스트: `tests/unit/test_query_analyzer.py` (유틸리티 검증)
- 통합 테스트: `tests/integration/test_nplusone.py` (비즈니스 로직 N+1 검증)

### 5.2 검증 결과

- `test_stocks_list_n_plus_one`: **PASSED** (2개의 쿼리로 데이터 5개/10개 조회 성공)
- `check_query_count`: **PASSED**

---

## 6. 문제 해결 (Troubleshooting)

### 6.1 Alembic Enum Type Issue

| 증상                                                      | 원인                                                               | 해결 방법                                                              |
| --------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `ProgrammingError: type "transactiontype" does not exist` | Alembic이 Enum 이름을 자동으로 생성하며 기존 DB 타입과 불일치 발생 | 모델 정의(`SQLEnum`)에 `name="transaction_type"` 등 명시적인 이름 부여 |

---

## 7. 결론 (Conclusion)

### 7.1 달성 사항

- 쿼리 효율성 검증 체계 구축 (N+1 방지)
- 대용량 데이터 대비 인덱싱 완료
- 성능 튜닝이 가능한 인프라(Connection Pool) 마련

### 7.2 다음 단계

- **Phase E**: Docker 및 CI/CD 구축을 통해 배포 파이프라인 자동화.
- 실제 운영 데이터 적재 후 `VACUUM` 및 인덱스 재구성 계획 수립 (장기 과제).
