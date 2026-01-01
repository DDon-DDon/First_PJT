# Phase 1: 데이터 모델 및 스키마 구현 보고서

**작성일**: 2026-01-01
**Phase**: 1.1 - SQLAlchemy 모델 / 1.2 - Pydantic 스키마
**TDD 단계**: 🔴 RED → 🟢 GREEN
**최종 상태**: ✅ Phase 1 완료 (27/27 테스트 통과)

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

## 5. 완료된 작업

### 5.1 모델 UUID → GUID 타입 변경 ✅
- [x] user.py - `from app.db.types import GUID` 적용
- [x] store.py - `Column(GUID, ...)` 변경 완료
- [x] category.py - GUID 타입 적용
- [x] product.py - id, category_id GUID 변경
- [x] transaction.py - id, product_id, store_id, user_id GUID 변경
- [x] stock.py - product_id, store_id GUID 변경 (복합키)

**변경 내용**:
```python
# 변경 전
from sqlalchemy.dialects.postgresql import UUID
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

# 변경 후
from app.db.types import GUID
id = Column(GUID, primary_key=True, default=uuid.uuid4)
```

### 5.2 테스트 실행 및 통과 확인 ✅

**테스트 실행 결과**:
```bash
$ pytest tests/test_models.py -v

============================= test session starts =============================
platform win32 -- Python 3.12.11, pytest-7.4.4, pluggy-1.6.0
collected 13 items

tests/test_models.py::TestUserModel::test_create_user PASSED             [  7%]
tests/test_models.py::TestUserModel::test_user_default_role PASSED       [ 15%]
tests/test_models.py::TestUserModel::test_user_email_unique PASSED       [ 23%]
tests/test_models.py::TestStoreModel::test_create_store PASSED           [ 30%]
tests/test_models.py::TestStoreModel::test_store_code_unique PASSED      [ 38%]
tests/test_models.py::TestCategoryModel::test_create_category PASSED     [ 46%]
tests/test_models.py::TestProductModel::test_create_product PASSED       [ 53%]
tests/test_models.py::TestProductModel::test_product_barcode_unique PASSED [ 61%]
tests/test_models.py::TestProductModel::test_product_default_safety_stock PASSED [ 69%]
tests/test_models.py::TestInventoryTransactionModel::test_create_inbound_transaction PASSED [ 76%]
tests/test_models.py::TestInventoryTransactionModel::test_create_adjust_transaction_with_reason PASSED [ 84%]
tests/test_models.py::TestCurrentStockModel::test_create_current_stock PASSED [ 92%]
tests/test_models.py::TestCurrentStockModel::test_current_stock_composite_key PASSED [100%]

======================= 13 passed, 35 warnings in 0.39s ==============================
```

**결과**: 🟢 **모든 테스트 통과 (13/13)**

**경고 사항**:
- `datetime.utcnow()` deprecation 경고 (Python 3.12+) - Phase 1.2에서 개선 예정

### 5.3 🔵 REFACTOR: 리팩토링 (Phase 1.2에서 진행 예정)
- [ ] Enum 타입 별도 파일로 분리
- [ ] 공통 Base 클래스 메서드 추가
- [ ] Relationship 설정 최적화
- [ ] datetime.utcnow() → datetime.now(UTC) 변경

### 5.4 커밋 ✅

**커밋 해시**: `d027231`

```bash
git commit -m "test: Add SQLAlchemy model tests (13 tests passed)

- User 모델 테스트 (3개): 생성, 기본 역할, 이메일 유니크
- Store 모델 테스트 (2개): 생성, 코드 유니크
- Category 모델 테스트 (1개): 생성
- Product 모델 테스트 (3개): 생성, 바코드 유니크, 안전재고 기본값
- InventoryTransaction 모델 테스트 (2개): 입고, 조정+사유
- CurrentStock 모델 테스트 (2개): 생성, 복합키

feat: Implement database models with GUID type

- User 모델 (UserRole Enum)
- Store 모델
- Category 모델
- Product 모델 (바코드 인덱스, 안전재고 기본값=10)
- InventoryTransaction 모델 (TransactionType, AdjustReason Enum)
- CurrentStock 모델 (복합 primary key)

fix: Add GUID type for SQLite compatibility

- PostgreSQL: UUID 타입 사용
- SQLite: CHAR(32) 타입 사용 (hex 저장)
- TypeDecorator로 플랫폼 독립적 구현

docs: Add Phase 1 implementation report

- 문제점 및 해결 방법 문서화
- pytest-asyncio 설정 해결 과정
- GUID 타입 구현 배경"
```

---

## 6. Phase 1.2: Pydantic 스키마 구현

**Phase**: 1.2 - Pydantic Request/Response 스키마
**TDD 단계**: 🔴 RED → 🟢 GREEN
**완료일**: 2026-01-01

### 6.1 작업 개요

#### 목표
- TDD 방식으로 Pydantic v2 스키마 구현
- Request/Response 스키마 분리
- FastAPI와 통합 가능한 데이터 검증 계층 구축

#### 구현한 스키마 (4개 모듈)
1. **common.py** - 공통 스키마 (Pagination, ErrorResponse, SuccessResponse)
2. **user.py** - 사용자 스키마 (UserCreate, UserResponse)
3. **product.py** - 제품 스키마 (ProductCreate, ProductResponse)
4. **transaction.py** - 트랜잭션 스키마 (InboundTransactionCreate, OutboundTransactionCreate, AdjustTransactionCreate, TransactionResponse)

---

### 6.2 🔴 RED: 테스트 작성

#### 테스트 파일
```
tests/test_schemas.py       # 스키마 검증 테스트 (14개)
```

#### 작성한 테스트 (총 14개)

**User 스키마 테스트 (4개)**
```python
class TestUserSchemas:
    def test_user_create_schema_valid()           # 정상 데이터 검증
    def test_user_create_schema_default_role()    # 기본 역할 = WORKER
    def test_user_create_schema_invalid_email()   # 이메일 검증 실패
    def test_user_response_schema()               # 응답 스키마 (password 제외)
```

**Product 스키마 테스트 (3개)**
```python
class TestProductSchemas:
    def test_product_create_schema_valid()            # 정상 데이터
    def test_product_create_schema_default_safety_stock()  # 안전재고 기본값=10
    def test_product_response_schema()                # 응답 스키마
```

**Transaction 스키마 테스트 (4개)**
```python
class TestTransactionSchemas:
    def test_inbound_transaction_create_schema()   # 입고 트랜잭션
    def test_outbound_transaction_create_schema()  # 출고 트랜잭션
    def test_adjust_transaction_create_schema()    # 조정 트랜잭션 (reason 필수)
    def test_transaction_response_schema()         # 트랜잭션 응답
```

**Common 스키마 테스트 (3개)**
```python
class TestCommonSchemas:
    def test_pagination_schema()       # 페이지네이션 (ge=1 검증)
    def test_error_response_schema()   # 에러 응답 (code, message, details)
    def test_success_response_schema() # 성공 응답 (success=True, data)
```

#### RED 단계 결과
```bash
$ pytest tests/test_schemas.py -v
# 14개 테스트 모두 FAILED (ImportError: No module named 'app.schemas')
```

🔴 **예상된 실패** - 스키마 파일이 없어 import 실패

---

### 6.3 🟢 GREEN: 스키마 구현

#### 구현한 스키마 파일
```
app/schemas/
├── __init__.py
├── common.py        # 공통 스키마
├── user.py          # 사용자 스키마
├── product.py       # 제품 스키마
└── transaction.py   # 트랜잭션 스키마
```

#### 주요 스키마 구현 내용

**common.py - 공통 응답 스키마**
```python
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict

class Pagination(BaseModel):
    """페이지네이션 정보"""
    page: int = Field(..., ge=1, description="현재 페이지")
    limit: int = Field(..., ge=1, le=100, description="페이지당 항목 수")
    total: int = Field(..., ge=0, description="전체 항목 수")
    totalPages: int = Field(..., ge=0, description="전체 페이지 수")

class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    code: str = Field(..., description="에러 코드")
    message: str = Field(..., description="에러 메시지")
    details: Optional[Dict[str, Any]] = Field(None, description="상세 정보")

class SuccessResponse(BaseModel):
    """성공 응답 스키마"""
    success: bool = Field(True, description="성공 여부")
    data: Any = Field(..., description="응답 데이터")
```

**특징**:
- API 응답 표준화 (성공/에러/페이지네이션)
- `Field` 제약조건으로 검증 강화 (ge, le)
- `details`는 Optional로 에러 상세정보 선택적 제공

**user.py - 사용자 스키마**
```python
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """사용자 생성 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    name: str = Field(..., min_length=1, max_length=100, description="이름")
    role: str = Field(default="WORKER", description="역할")

class UserResponse(BaseModel):
    """사용자 응답 스키마"""
    id: UUID
    email: EmailStr
    name: str
    role: str
    isActive: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}
```

**특징**:
- `EmailStr` - email-validator로 이메일 검증
- `password` - 최소 6자 검증 (min_length)
- `UserResponse` - password 제외 (보안)
- `model_config` - SQLAlchemy 모델과 호환

**product.py - 제품 스키마**
```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    """제품 생성 요청 스키마"""
    barcode: str = Field(..., min_length=1, max_length=50, description="바코드")
    name: str = Field(..., min_length=1, max_length=200, description="제품명")
    categoryId: str = Field(..., description="카테고리 ID")
    safetyStock: int = Field(default=10, ge=0, description="안전재고")
    imageUrl: Optional[str] = Field(None, max_length=500, description="이미지 URL")
    memo: Optional[str] = Field(None, description="메모")

class ProductResponse(BaseModel):
    """제품 응답 스키마"""
    id: UUID
    barcode: str
    name: str
    categoryId: UUID
    safetyStock: int
    imageUrl: Optional[str]
    memo: Optional[str]
    isActive: bool
    createdAt: datetime
    updatedAt: Optional[datetime]

    model_config = {"from_attributes": True}
```

**특징**:
- `safetyStock` - 기본값 10, 0 이상 검증 (ge=0)
- camelCase 필드명 (프론트엔드 호환)
- 선택적 필드: imageUrl, memo

**transaction.py - 트랜잭션 스키마**
```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class InboundTransactionCreate(BaseModel):
    """입고 트랜잭션 생성 요청"""
    productId: str = Field(..., description="제품 ID")
    storeId: str = Field(..., description="매장 ID")
    quantity: int = Field(..., gt=0, description="입고 수량")
    note: Optional[str] = Field(None, description="비고")

class OutboundTransactionCreate(BaseModel):
    """출고 트랜잭션 생성 요청"""
    productId: str
    storeId: str
    quantity: int = Field(..., gt=0, description="출고 수량")
    note: Optional[str] = None

class AdjustTransactionCreate(BaseModel):
    """조정 트랜잭션 생성 요청"""
    productId: str
    storeId: str
    quantity: int = Field(..., description="조정 수량")
    reason: str = Field(..., description="조정 사유")
    note: Optional[str] = None

class TransactionResponse(BaseModel):
    """트랜잭션 응답 스키마"""
    id: UUID
    productId: UUID
    storeId: UUID
    userId: UUID
    type: str
    quantity: int
    reason: Optional[str]
    note: Optional[str]
    createdAt: datetime
    syncedAt: Optional[datetime]

    model_config = {"from_attributes": True}
```

**특징**:
- 트랜잭션 타입별 스키마 분리
- 입고/출고: `quantity > 0` 검증 (gt=0)
- 조정: `reason` 필수, quantity는 음수 가능
- `syncedAt` - 오프라인 동기화 상태 추적

---

### 6.4 발생한 문제점 및 해결

#### 🚨 문제: email-validator 미설치

**문제 상황**
```
ModuleNotFoundError: No module named 'email_validator'
ImportError: email-validator is not installed
```

Pydantic의 `EmailStr` 타입을 사용하려면 별도의 email-validator 패키지가 필요한데 설치되어 있지 않음.

**원인**
- `pydantic==2.5.3`만 설치됨
- `EmailStr`은 `email-validator` 패키지에 의존

**해결 방법**
```bash
cd backend && uv pip install email-validator
# Installed: dnspython==2.8.0, email-validator==2.3.0
```

**requirements.txt 업데이트**
```python
# Data Validation
pydantic==2.5.3
pydantic-settings==2.1.0
email-validator==2.3.0  # ✅ 추가
```

**결과**: ✅ 모든 테스트 통과 (14/14)

---

### 6.5 테스트 실행 및 통과 확인 ✅

**테스트 실행 결과**:
```bash
$ pytest tests/test_schemas.py -v

============================= test session starts =============================
collected 14 items

tests/test_schemas.py::TestUserSchemas::test_user_create_schema_valid PASSED [ 7%]
tests/test_schemas.py::TestUserSchemas::test_user_create_schema_default_role PASSED [ 14%]
tests/test_schemas.py::TestUserSchemas::test_user_create_schema_invalid_email PASSED [ 21%]
tests/test_schemas.py::TestUserSchemas::test_user_response_schema PASSED [ 28%]
tests/test_schemas.py::TestProductSchemas::test_product_create_schema_valid PASSED [ 35%]
tests/test_schemas.py::TestProductSchemas::test_product_create_schema_default_safety_stock PASSED [ 42%]
tests/test_schemas.py::TestProductSchemas::test_product_response_schema PASSED [ 50%]
tests/test_schemas.py::TestTransactionSchemas::test_inbound_transaction_create_schema PASSED [ 57%]
tests/test_schemas.py::TestTransactionSchemas::test_outbound_transaction_create_schema PASSED [ 64%]
tests/test_schemas.py::TestTransactionSchemas::test_adjust_transaction_create_schema PASSED [ 71%]
tests/test_schemas.py::TestTransactionSchemas::test_transaction_response_schema PASSED [ 78%]
tests/test_schemas.py::TestCommonSchemas::test_pagination_schema PASSED [ 85%]
tests/test_schemas.py::TestCommonSchemas::test_error_response_schema PASSED [ 92%]
tests/test_schemas.py::TestCommonSchemas::test_success_response_schema PASSED [100%]

======================= 14 passed, 3 warnings in 0.11s =======================
```

**결과**: 🟢 **모든 테스트 통과 (14/14)**

---

### 6.6 Phase 1.2 커밋 ✅

**커밋 해시**: `447b2a7`

```bash
git commit -m "test: Add Pydantic schema validation tests (14 tests passed)

- User 스키마 테스트 (4개): 생성, 기본역할, 이메일검증, 응답
- Product 스키마 테스트 (3개): 생성, 안전재고 기본값, 응답
- Transaction 스키마 테스트 (4개): 입고, 출고, 조정, 응답
- Common 스키마 테스트 (3개): 페이지네이션, 에러, 성공응답

feat: Implement Pydantic v2 schemas for API layer

- common.py: Pagination, ErrorResponse, SuccessResponse
- user.py: UserCreate, UserResponse (EmailStr validation)
- product.py: ProductCreate, ProductResponse
- transaction.py: InboundTransactionCreate, OutboundTransactionCreate, AdjustTransactionCreate, TransactionResponse

fix: Add email-validator dependency

- email-validator==2.3.0 추가
- Pydantic EmailStr 타입 지원

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### 6.7 Phase 1.2에서 구현한 파일

**새로 생성된 파일**
```
✅ tests/test_schemas.py             (246줄) - 스키마 검증 테스트 14개
✅ app/schemas/__init__.py            (0줄)   - 스키마 패키지
✅ app/schemas/common.py              (27줄)  - 공통 스키마
✅ app/schemas/user.py                (31줄)  - 사용자 스키마
✅ app/schemas/product.py             (34줄)  - 제품 스키마
✅ app/schemas/transaction.py         (54줄)  - 트랜잭션 스키마
```

**수정된 파일**
```
✅ backend/requirements.txt           - email-validator==2.3.0 추가
```

---

## 7. 테스트 커버리지 목표 (Phase 1 전체)

| 영역 | Phase 1.1 | Phase 1.2 | 전체 | 목표 |
|------|-----------|-----------|------|------|
| SQLAlchemy Models | 13개 테스트 ✅ | - | 13개 | 13개 ✅ |
| Pydantic Schemas | - | 14개 테스트 ✅ | 14개 | 14개 ✅ |
| **전체** | **13개** | **14개** | **27개** | **27개 ✅** |
| 모델 개수 | 6개 ✅ | - | 6개 | 6개 ✅ |
| 스키마 모듈 | - | 4개 ✅ | 4개 | 4개 ✅ |

---

## 8. Phase 1 전체 실행 결과 ✅

**최종 테스트 실행**:
```bash
$ pytest tests/ -v

============================= test session starts =============================
collected 27 items

tests/test_models.py::TestUserModel::test_create_user PASSED             [  3%]
tests/test_models.py::TestUserModel::test_user_default_role PASSED       [  7%]
tests/test_models.py::TestUserModel::test_user_email_unique PASSED       [ 11%]
tests/test_models.py::TestStoreModel::test_create_store PASSED           [ 14%]
tests/test_models.py::TestStoreModel::test_store_code_unique PASSED      [ 18%]
tests/test_models.py::TestCategoryModel::test_create_category PASSED     [ 22%]
tests/test_models.py::TestProductModel::test_create_product PASSED       [ 25%]
tests/test_models.py::TestProductModel::test_product_barcode_unique PASSED [ 29%]
tests/test_models.py::TestProductModel::test_product_default_safety_stock PASSED [ 33%]
tests/test_models.py::TestInventoryTransactionModel::test_create_inbound_transaction PASSED [ 37%]
tests/test_models.py::TestInventoryTransactionModel::test_create_adjust_transaction_with_reason PASSED [ 40%]
tests/test_models.py::TestCurrentStockModel::test_create_current_stock PASSED [ 44%]
tests/test_models.py::TestCurrentStockModel::test_current_stock_composite_key PASSED [ 48%]
tests/test_schemas.py::TestUserSchemas::test_user_create_schema_valid PASSED [ 51%]
tests/test_schemas.py::TestUserSchemas::test_user_create_schema_default_role PASSED [ 55%]
tests/test_schemas.py::TestUserSchemas::test_user_create_schema_invalid_email PASSED [ 59%]
tests/test_schemas.py::TestUserSchemas::test_user_response_schema PASSED [ 62%]
tests/test_schemas.py::TestProductSchemas::test_product_create_schema_valid PASSED [ 66%]
tests/test_schemas.py::TestProductSchemas::test_product_create_schema_default_safety_stock PASSED [ 70%]
tests/test_schemas.py::TestProductSchemas::test_product_response_schema PASSED [ 74%]
tests/test_schemas.py::TestTransactionSchemas::test_inbound_transaction_create_schema PASSED [ 77%]
tests/test_schemas.py::TestTransactionSchemas::test_outbound_transaction_create_schema PASSED [ 81%]
tests/test_schemas.py::TestTransactionSchemas::test_adjust_transaction_create_schema PASSED [ 85%]
tests/test_schemas.py::TestTransactionSchemas::test_transaction_response_schema PASSED [ 88%]
tests/test_schemas.py::TestCommonSchemas::test_pagination_schema PASSED  [ 92%]
tests/test_schemas.py::TestCommonSchemas::test_error_response_schema PASSED [ 96%]
tests/test_schemas.py::TestCommonSchemas::test_success_response_schema PASSED [100%]

======================= 27 passed, 38 warnings in 0.42s =======================
```

**결과**: 🟢 **Phase 1 완료 - 27/27 테스트 통과**

---

## 9. 배운 점 (Lessons Learned)

### TDD 효과
1. **명확한 요구사항**: 테스트를 먼저 작성하니 필요한 필드/제약조건이 명확해짐
2. **빠른 피드백**: 구현 직후 바로 테스트로 검증 가능
3. **리팩토링 안전망**: 테스트가 있어 수정 시 안심
4. **레이어 분리**: 모델(DB)과 스키마(API) 분리로 관심사 분리 명확

### 기술적 발견

#### Phase 1.1 (Models)
1. **pytest-asyncio**: `asyncio_mode = auto` 설정으로 간편한 비동기 테스트
2. **TypeDecorator**: SQLAlchemy에서 커스텀 타입 구현 방법 습득
3. **Fixture 격리**: 테스트마다 테이블 생성/삭제로 완전한 격리

#### Phase 1.2 (Schemas)
1. **Pydantic v2**: `model_config = {"from_attributes": True}`로 ORM 모델 호환
2. **EmailStr 검증**: email-validator 패키지로 이메일 자동 검증
3. **Field 제약조건**: `gt=0`, `ge=1`, `min_length` 등으로 데이터 검증 강화
4. **Request/Response 분리**: Create 스키마는 입력 검증, Response는 출력 직렬화

### 주의사항

#### Phase 1.1 (Models)
1. **DB 호환성**: 테스트 DB와 운영 DB가 다를 경우 타입 호환성 체크 필수
2. **비동기 테스트**: fixture와 테스트 함수 모두 `async/await` 일관성 유지
3. **복합키**: CurrentStock처럼 복합 Primary Key는 유니크 제약 테스트 필수

#### Phase 1.2 (Schemas)
1. **의존성 관리**: Pydantic의 특수 타입(EmailStr 등)은 추가 패키지 필요
2. **snake_case vs camelCase**: Python 모델은 snake_case, API 스키마는 camelCase 사용
3. **보안**: Response 스키마에서 민감 정보(password 등) 제외 필수

---

## 10. 파일 변경 내역 (Phase 1 전체)

### Phase 1.1 - 새로 생성된 파일
```
✅ tests/conftest.py                 (128줄) - pytest 설정 및 fixtures
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

### Phase 1.2 - 새로 생성된 파일
```
✅ tests/test_schemas.py             (246줄) - 스키마 검증 테스트 14개
✅ app/schemas/__init__.py            (0줄)   - 스키마 패키지
✅ app/schemas/common.py              (27줄)  - 공통 스키마
✅ app/schemas/user.py                (31줄)  - 사용자 스키마
✅ app/schemas/product.py             (34줄)  - 제품 스키마
✅ app/schemas/transaction.py         (54줄)  - 트랜잭션 스키마
```

### Phase 1.1 - 수정된 파일
```
✅ app/models/user.py                - UUID → GUID 타입 변경
✅ app/models/store.py               - UUID → GUID 타입 변경
✅ app/models/category.py            - UUID → GUID 타입 변경
✅ app/models/product.py             - UUID → GUID 타입 변경
✅ app/models/transaction.py         - UUID → GUID 타입 변경
✅ app/models/stock.py               - UUID → GUID 타입 변경
```

### Phase 1.2 - 수정된 파일
```
✅ backend/requirements.txt          - email-validator==2.3.0 추가
```

### Phase 1 전체 요약
- **새로 생성된 파일**: 16개
  - 테스트 파일: 3개 (conftest.py, test_models.py, test_schemas.py)
  - 모델 파일: 7개 (models 6개 + types.py)
  - 스키마 파일: 5개 (schemas 4개 + __init__.py)
  - 설정 파일: 1개 (pytest.ini)
- **수정된 파일**: 7개
  - 모델 GUID 변경: 6개
  - 의존성 추가: 1개 (requirements.txt)

---

## 11. 커밋 히스토리

### Phase 1.1 커밋
- **커밋 해시**: `d027231`
- **커밋 메시지**: test: Add SQLAlchemy model tests (13 tests passed)
- **포함 내용**: 모델 6개, 테스트 13개, GUID 타입

### Phase 1.2 커밋
- **커밋 해시**: `447b2a7`
- **커밋 메시지**: test: Add Pydantic schema validation tests (14 tests passed)
- **포함 내용**: 스키마 4개 모듈, 테스트 14개, email-validator 의존성

---

## 12. 참조

- [TDD 로드맵](./tdd-roadmap.md)
- [ERD 명세](../.claude/skills/ddon-project/references/erd.md)
- [DB 스키마](../backend/init-db/01-schema.sql)
- [Phase 1.1 커밋](https://github.com/DDon-DDon/ddon-backend/commit/d027231)
- [Phase 1.2 커밋](https://github.com/DDon-DDon/ddon-backend/commit/447b2a7)

---

**작성자**: Claude Code
**상태**: ✅ TDD Phase 1 완료 (2026-01-01)
**완료 항목**:
- Phase 1.1: SQLAlchemy 모델 구현 (13개 테스트 통과)
- Phase 1.2: Pydantic 스키마 구현 (14개 테스트 통과)
- **전체**: 27개 테스트 통과 ✅

**다음 단계**: Phase 2 - Authentication API 구현 (TDD 방식)
