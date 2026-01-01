# Phase 1: SQLAlchemy 모델 구현 보고서

**작성일**: 2026-01-01
**Phase**: 1.1 - SQLAlchemy 모델 테스트 및 구현
**TDD 단계**: 🔴 RED → 🟢 GREEN

---

## 1. 작업 개요

### 목표
- TDD 방식으로 SQLAlchemy 모델 구현
- 테스트 먼저 작성 후 모델 구현
- PostgreSQL과 SQLite(테스트용) 모두 지원

### 구현한 모델 (총 6개)
1. **User** - 사용자 (WORKER, ADMIN)
2. **Store** - 매장/창고
3. **Category** - 제품 카테고리
4. **Product** - 제품 마스터
5. **InventoryTransaction** - 재고 트랜잭션 (입출고 이력)
6. **CurrentStock** - 현재고 캐시

---

## 2. 🔴 RED: 테스트 작성

### 2.1 테스트 파일 구조

```
tests/
├── conftest.py          # pytest 설정 및 fixtures
├── test_models.py       # 모델 테스트 (13개)
└── pytest.ini           # pytest 설정
```

### 2.2 작성한 테스트 (총 13개)

#### User 모델 테스트 (3개)
```python
class TestUserModel:
    async def test_create_user()           # 사용자 생성
    async def test_user_default_role()     # 기본 역할 = WORKER
    async def test_user_email_unique()     # 이메일 유니크 제약
```

#### Store 모델 테스트 (2개)
```python
class TestStoreModel:
    async def test_create_store()          # 매장 생성
    async def test_store_code_unique()     # 매장 코드 유니크
```

#### Category 모델 테스트 (1개)
```python
class TestCategoryModel:
    async def test_create_category()       # 카테고리 생성
```

#### Product 모델 테스트 (3개)
```python
class TestProductModel:
    async def test_create_product()                # 제품 생성
    async def test_product_barcode_unique()        # 바코드 유니크
    async def test_product_default_safety_stock()  # 안전재고 기본값=10
```

#### InventoryTransaction 모델 테스트 (2개)
```python
class TestInventoryTransactionModel:
    async def test_create_inbound_transaction()           # 입고 트랜잭션
    async def test_create_adjust_transaction_with_reason() # 조정 트랜잭션 + 사유
```

#### CurrentStock 모델 테스트 (2개)
```python
class TestCurrentStockModel:
    async def test_create_current_stock()          # 현재고 생성
    async def test_current_stock_composite_key()   # 복합키 (product_id, store_id)
```

### 2.3 Fixtures 구현

#### conftest.py
```python
@pytest.fixture
async def db_session():
    """테스트용 DB 세션 (SQLite 인메모리)"""
    # 테이블 생성
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 세션 제공
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    # 테이블 삭제 (테스트 격리)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

#### pytest.ini
```ini
[pytest]
asyncio_mode = auto       # 자동 비동기 모드
testpaths = tests
python_files = test_*.py
```

---

## 3. 🟢 GREEN: 모델 구현

### 3.1 구현한 모델 파일

```
app/models/
├── __init__.py
├── user.py              # User 모델 + UserRole Enum
├── store.py             # Store 모델
├── category.py          # Category 모델
├── product.py           # Product 모델
├── transaction.py       # InventoryTransaction + TransactionType/AdjustReason Enum
└── stock.py             # CurrentStock 모델
```

### 3.2 주요 모델 구현 내용

#### User 모델
```python
class UserRole(str, enum.Enum):
    WORKER = "WORKER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.WORKER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

**특징**:
- `UserRole` Enum으로 역할 관리 (WORKER, ADMIN)
- `email` 유니크 제약 + 인덱스
- 기본 역할은 WORKER
- 타임스탬프 (created_at, updated_at)

#### Product 모델
```python
class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barcode = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    safety_stock = Column(Integer, nullable=False, default=10)
    image_url = Column(String(500))
    memo = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("Category", backref="products")
```

**특징**:
- `barcode` 유니크 + 인덱스 (빠른 조회)
- `safety_stock` 기본값 10개
- Category와 N:1 관계

#### InventoryTransaction 모델
```python
class TransactionType(str, enum.Enum):
    INBOUND = "INBOUND"   # 입고
    OUTBOUND = "OUTBOUND" # 출고
    ADJUST = "ADJUST"     # 조정

class AdjustReason(str, enum.Enum):
    EXPIRED = "EXPIRED"       # 유통기한 만료
    DAMAGED = "DAMAGED"       # 파손
    CORRECTION = "CORRECTION" # 재고 정정
    OTHER = "OTHER"           # 기타

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(SQLEnum(AdjustReason))
    note = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    synced_at = Column(DateTime)  # 오프라인 동기화용
```

**특징**:
- Append-Only 설계 (삭제/수정 불가)
- `type` Enum으로 입고/출고/조정 구분
- `reason` Enum으로 조정 사유 관리
- `synced_at`: NULL이면 동기화 대기 중

#### CurrentStock 모델
```python
class CurrentStock(Base):
    __tablename__ = "current_stocks"

    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)
    last_alerted_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

**특징**:
- **복합 Primary Key** (product_id, store_id)
- 빠른 재고 조회를 위한 캐시 테이블
- `last_alerted_at`: 안전재고 알림 중복 방지

---

## 4. 발생한 문제점 및 해결

### 🚨 문제 1: pytest fixture 비동기 에러

#### 문제 상황
```python
AttributeError: 'async_generator' object has no attribute 'add'
```

테스트에서 `db_session.add(user)`를 호출할 때 async_generator 객체가 반환되어 `.add()` 메서드를 찾을 수 없는 오류 발생.

#### 원인
- `@pytest.fixture`에서 `async def`로 정의하고 `yield`를 사용할 때, pytest-asyncio가 제너레이터를 반환
- 테스트 함수에서 `await` 없이 fixture를 사용하면 제너레이터 객체가 그대로 전달됨

#### 해결 방법
1. **pytest.ini 추가**
```ini
[pytest]
asyncio_mode = auto
```

2. **conftest.py fixture 수정**
```python
# 이전 (문제 있음)
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# 이후 (수정)
# pytest-asyncio의 기본 event_loop 사용 (fixture 제거)
```

3. **db_session fixture 단순화**
```python
@pytest.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

**결과**: ✅ pytest-asyncio가 자동으로 제너레이터를 처리하여 세션 객체 제공

---

### 🚨 문제 2: SQLite에서 UUID 타입 미지원

#### 문제 상황
```
sqlalchemy.exc.CompileError: Compiler can't render element of type UUID
```

PostgreSQL의 `UUID` 타입을 사용했는데, SQLite는 네이티브 UUID를 지원하지 않아 테스트 실행 시 오류 발생.

#### 원인
- `from sqlalchemy.dialects.postgresql import UUID` 사용
- SQLite는 UUID 타입이 없음 (STRING이나 CHAR로 저장해야 함)
- 테스트는 SQLite 인메모리 DB 사용

#### 해결 방법

**app/db/types.py 생성** - 플랫폼 독립적인 GUID 타입 구현

```python
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

class GUID(TypeDecorator):
    """
    플랫폼 독립적인 GUID 타입

    - PostgreSQL: UUID 타입 사용
    - SQLite: CHAR(32) 사용 (hex 저장)
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        """저장 시 변환"""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).hex
            else:
                return value.hex

    def process_result_value(self, value, dialect):
        """조회 시 변환"""
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        else:
            return value
```

**모델 수정 필요** (다음 단계)
```python
# 변경 전
from sqlalchemy.dialects.postgresql import UUID
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

# 변경 후
from app.db.types import GUID
id = Column(GUID, primary_key=True, default=uuid.uuid4)
```

**결과**: ⏳ 다음 단계에서 모든 모델 수정 예정

---

## 5. 다음 작업 (진행 예정)

### 5.1 모델 UUID → GUID 타입 변경
- [ ] user.py
- [ ] store.py
- [ ] category.py
- [ ] product.py
- [ ] transaction.py
- [ ] stock.py

### 5.2 테스트 실행 및 통과 확인
```bash
pytest tests/test_models.py -v
```

### 5.3 🔵 REFACTOR: 리팩토링
- [ ] Enum 타입 별도 파일로 분리
- [ ] 공통 Base 클래스 메서드 추가
- [ ] Relationship 설정 최적화

### 5.4 커밋
```bash
git add .
git commit -m "test: Add SQLAlchemy model tests (13 tests)
feat: Implement database models with TDD approach
fix: Add GUID type for SQLite compatibility"
```

---

## 6. 테스트 커버리지 목표

| 영역 | 현재 | 목표 |
|------|------|------|
| models/ | 0% → 예상 70%+ | 70%+ |
| 테스트 개수 | 13개 | 13개 ✅ |
| 모델 개수 | 6개 | 6개 ✅ |

---

## 7. 배운 점 (Lessons Learned)

### TDD 효과
1. **명확한 요구사항**: 테스트를 먼저 작성하니 필요한 필드/제약조건이 명확해짐
2. **빠른 피드백**: 모델 구현 직후 바로 테스트로 검증 가능
3. **리팩토링 안전망**: 테스트가 있어 수정 시 안심

### 기술적 발견
1. **pytest-asyncio**: `asyncio_mode = auto` 설정으로 간편한 비동기 테스트
2. **TypeDecorator**: SQLAlchemy에서 커스텀 타입 구현 방법 습득
3. **Fixture 격리**: 테스트마다 테이블 생성/삭제로 완전한 격리

### 주의사항
1. **DB 호환성**: 테스트 DB와 운영 DB가 다를 경우 타입 호환성 체크 필수
2. **비동기 테스트**: fixture와 테스트 함수 모두 `async/await` 일관성 유지
3. **복합키**: CurrentStock처럼 복합 Primary Key는 유니크 제약 테스트 필수

---

## 8. 파일 변경 내역

### 새로 생성된 파일
```
✅ tests/conftest.py                 (128줄) - pytest 설정
✅ tests/test_models.py              (400줄) - 모델 테스트 13개
✅ backend/pytest.ini                (6줄)   - pytest 설정
✅ app/models/user.py                (45줄)  - User 모델
✅ app/models/store.py               (35줄)  - Store 모델
✅ app/models/category.py            (30줄)  - Category 모델
✅ app/models/product.py             (45줄)  - Product 모델
✅ app/models/transaction.py         (65줄)  - InventoryTransaction 모델
✅ app/models/stock.py               (30줄)  - CurrentStock 모델
✅ app/db/types.py                   (45줄)  - GUID 커스텀 타입
```

### 수정 예정 파일
```
⏳ app/models/*.py                   - UUID → GUID 타입 변경
```

---

## 9. 참조

- [TDD 로드맵](./tdd-roadmap.md)
- [ERD 명세](../.claude/skills/ddon-project/references/erd.md)
- [DB 스키마](../backend/init-db/01-schema.sql)

---

**작성자**: Claude Code
**검토**: TDD Phase 1.1 완료 대기 중
