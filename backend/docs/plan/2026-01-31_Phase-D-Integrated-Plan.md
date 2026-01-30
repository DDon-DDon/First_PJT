# Phase D 통합 구현 계획: 쿼리 최적화 & 벤치마크

**Phase**: D (Query Optimization & Benchmark)
**기간**: 2026-01-31 ~ (4-5일 예상)
**전략**: 선(先) 구현 및 최적화, 후(後) 검증 및 벤치마크

---

## 1. 개요

백엔드 시스템의 성능 병목을 제거하고, 안정적인 운영을 위한 데이터베이스 최적화를 수행합니다.
쿼리 분석 환경 구축부터 N+1 문제 해결, 인덱스 최적화, 커넥션 풀 튜닝을 거쳐 최종적으로 벤치마크를 통해 성능 개선을 입증합니다.

## 2. 세부 태스크 및 구현 순서

### ✅ D-1: 쿼리 분석 환경 구축 (완료)

**목표**: 쿼리 실행 계획 분석 및 모니터링 기반 마련

- [x] Query Analyzer 유틸리티 구현 (`app/core/query_analyzer.py`)
- [x] Connection Pool 로깅 설정 (`app/db/session.py`)

### 🚀 D-2: N+1 문제 점검 및 해결

**목표**: ORM 사용 시 발생하는 비효율적인 추가 쿼리 제거

- **타겟**: `app/api/v1/inventory.py` (재고 조회), `app/api/v1/projects.py` (상품 조회)
- **전략**:
  - `QueryCounter`로 N+1 발생 지점 탐지
  - SQLAlchemy `selectinload` (1:N), `joinedload` (N:1) 옵션 적용
  - 필요한 경우 ViewModel/Schema 구조에 맞춰 쿼리 재작성

### 🚀 D-3: 인덱스 최적화

**목표**: Full Table Scan을 Index Scan으로 전환하여 조회 속도 향상

- **분석**: `explain_analyze` 유틸리티로 슬로우 쿼리 식별
- **구현**:
  - `current_stocks` (store_id, product_id) 복합 인덱스
  - `inventory_transactions` (created_at) 정렬 인덱스
  - `products` (barcode) 유니크 인덱스 확인
- **적용**: Alembic 마이그레이션 스크립트 작성 (`alembic revision`)

### 🚀 D-4: Connection Pool 튜닝 (보완)

**목표**: 고부하 상황에서도 안정적인 DB 연결 유지

- [x] `pool_recycle`, `pool_timeout` (D-1에서 선반영됨)
- **추가 작업**:
  - 프로덕션 환경용 Pool Size 최적값 산정 및 적용 (`settings.DB_POOL_SIZE`)
  - 부하 테스트 시 연결 고갈 모니터링

### 📊 D-5: 벤치마크 및 성능 기준선

**목표**: 최적화 전후 성능 비교 및 리포트 작성

- **도구**: Locust (부하 테스트), Pytest-Benchmark (단위 성능)
- **시나리오**:
  - 사용자 시나리오: 재고 목록 조회 (Pagination 포함)
  - 관리자 시나리오: 대량 재고 업데이트
- **산출물**: 성능 리포트 (`docs/implemented/2026-02-xx_phase-d-benchmark.md`)

---

## 3. 상세 구현 가이드

### [D-2] N+1 해결 패턴

**수정 파일**: `app/crud/inventory.py` (예시)

```python
# Before
result = await session.execute(select(CurrentStock).where(...))
stocks = result.scalars().all()
# stock.product 접근 시 Lazy Loading 발생

# After
result = await session.execute(
    select(CurrentStock)
    .where(...)
    .options(
        joinedload(CurrentStock.product),
        selectinload(CurrentStock.product.category)
    )
)
```

### [D-3] 인덱스 마이그레이션

**명령어**:

```bash
alembic revision -m "add indexes for optimization"
```

**마이그레이션 파일**:

```python
def upgrade():
    op.create_index(
        'idx_current_stocks_lookup',
        'current_stocks',
        ['store_id', 'product_id']
    )
```

### [D-5] 벤치마크 시나리오

**파일**: `tests/load/locustfile.py`

```python
class UserBehavior(TaskSet):
    @task
    def get_inventory(self):
        self.client.get("/api/v1/inventory?store_id=...")
```

---

## 4. 검증 및 완료 조건

1. **단위 테스트**: `test_query_analyzer.py` 등 관련 테스트 통과
2. **N+1 제거**: 주요 조회 API에서 쿼리 수가 데이터 양에 비례하지 않음 (상수 시간 복잡도)
3. **인덱스 활용**: EXPLAIN 결과 `Seq Scan`이 `Index Scan`으로 변경됨
4. **성능 개선**: 최적화 후 응답 시간(P95) 감소 확인

---

## 5. 작업 진행 순서

1. **계획 승인 및 D-2 착수**
2. D-2 구현 (코드 수정)
3. D-3 인덱스 추가 (마이그레이션)
4. D-4 설정 검토
5. D-5 벤치마킹 수행 및 리포트 작성
