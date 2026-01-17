# 2. 프로젝트 구조

이 문서에서는 **레이어 아키텍처**의 개념과 프로젝트 폴더 구조가 **왜 이렇게 설계되었는지**를 설명합니다.

---

## 📌 아키텍처 개요

### 레이어 아키텍처 (Layered Architecture)

```
┌──────────────────────────────────────────────────────────────┐
│                    🌐 Presentation Layer                     │
│                    (API / Controllers)                       │
│         HTTP 요청/응답 처리, 라우팅, 인증                        │
├──────────────────────────────────────────────────────────────┤
│                    💼 Business Layer                         │
│                    (Services)                                │
│         비즈니스 로직, 트랜잭션 관리, 유스케이스                   │
├──────────────────────────────────────────────────────────────┤
│                    📊 Data Layer                             │
│                    (Models + Schemas)                        │
│         데이터 정의, 검증, 영속성                               │
├──────────────────────────────────────────────────────────────┤
│                    🗄️ Infrastructure                         │
│                    (Database / External)                     │
│         PostgreSQL, 외부 API, 파일 시스템                      │
└──────────────────────────────────────────────────────────────┘
```

### 왜 레이어 아키텍처인가?

| 원칙              | 설명                                       |
| ----------------- | ------------------------------------------ |
| **관심사 분리**   | 각 레이어는 하나의 책임만 가짐             |
| **의존성 방향**   | 상위 레이어 → 하위 레이어로만 의존         |
| **테스트 용이성** | 각 레이어를 독립적으로 테스트 가능         |
| **유지보수성**    | 한 레이어 변경이 다른 레이어에 영향 최소화 |

---

## 📁 폴더 구조

```
backend/
├── alembic/                    # 🗄️ DB 마이그레이션
│   ├── versions/               # 마이그레이션 히스토리
│   └── env.py                  # Alembic 환경 설정
│
├── app/                        # 📦 애플리케이션 코드
│   ├── main.py                 # 🚀 앱 진입점
│   │
│   ├── api/                    # 🌐 Presentation Layer
│   │   ├── __init__.py
│   │   ├── deps.py             # 공통 의존성
│   │   └── v1/                 # API 버전 1
│   │       ├── products.py
│   │       ├── inventory.py
│   │       ├── transactions.py
│   │       ├── sync.py
│   │       └── admin.py
│   │
│   ├── services/               # 💼 Business Layer
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── sync.py
│   │   └── report.py
│   │
│   ├── models/                 # 📊 Data Layer (ORM)
│   │   ├── user.py
│   │   ├── store.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   ├── stock.py
│   │   └── user_store.py
│   │
│   ├── schemas/                # 📊 Data Layer (Validation)
│   │   ├── common.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   └── sync.py
│   │
│   ├── core/                   # ⚙️ Configuration
│   │   ├── config.py           # 환경 변수
│   │   ├── security.py         # JWT, 암호화
│   │   └── exceptions.py       # 커스텀 예외
│   │
│   └── db/                     # 🗄️ Database
│       ├── base.py             # Base 클래스
│       ├── session.py          # 세션 팩토리
│       └── types.py            # GUID 타입
│
├── tests/                      # 🧪 테스트
│   ├── conftest.py
│   ├── test_products.py
│   └── test_e2e.py
│
└── docs/                       # 📚 문서
    ├── implemented/            # 구현 리포트
    ├── roadmap/                # 로드맵
    └── manual/                 # 이 메뉴얼
```

---

## 🎯 각 폴더의 역할

### 1. `app/api/` - Presentation Layer

> HTTP 요청을 받아 적절한 서비스로 전달하고 응답을 반환

**포함 내용:**

- FastAPI 라우터 (`APIRouter`)
- 경로 파라미터 처리
- 요청/응답 스키마 연결
- 인증/권한 체크

**규칙:**

```python
# ✅ 좋은 예: 서비스에 위임
@router.post("/products")
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await product_service.create(db, data, user)

# ❌ 나쁜 예: 라우터에 비즈니스 로직
@router.post("/products")
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Product).where(Product.barcode == data.barcode))
    if existing.scalar():
        raise HTTPException(409, "Duplicate")
    product = Product(**data.dict())
    db.add(product)
    await db.commit()
    return product
```

---

### 2. `app/services/` - Business Layer

> 핵심 비즈니스 로직과 유스케이스 구현

**포함 내용:**

- 입출고 처리 로직
- 재고 계산
- 동기화 로직
- 리포트 생성

**규칙:**

```python
# services/inventory.py
async def process_outbound(
    db: AsyncSession,
    data: OutboundCreate,
    user: User
) -> TransactionResult:
    # 1. 재고 조회
    stock = await _get_current_stock(db, data.product_id, data.store_id)

    # 2. 비즈니스 검증
    if stock.quantity < data.quantity:
        raise InsufficientStockException(...)

    # 3. 재고 감소
    stock.quantity -= data.quantity

    # 4. 트랜잭션 기록
    transaction = InventoryTransaction(...)
    db.add(transaction)

    # 5. 안전재고 알림 체크
    safety_alert = stock.quantity < stock.product.safety_stock

    return TransactionResult(new_stock=stock.quantity, safety_alert=safety_alert)
```

**왜 서비스 레이어를 분리하는가?**

1. **재사용성**: 동일 로직을 여러 API에서 사용
2. **테스트 용이성**: HTTP 컨텍스트 없이 비즈니스 로직 테스트
3. **트랜잭션 관리**: 여러 DB 작업을 하나의 트랜잭션으로 묶음

---

### 3. `app/models/` - Data Layer (ORM)

> 데이터베이스 테이블 구조 정의

**포함 내용:**

- SQLAlchemy 모델 클래스
- 테이블 컬럼 정의
- 관계 (Relationship) 정의
- 인덱스 정의

**예시:**

```python
# models/product.py
class Product(Base):
    __tablename__ = "products"  # (Base에서 자동 생성됨)

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    barcode = Column(String(50), unique=True, index=True)  # 인덱스
    name = Column(String(200), nullable=False)
    category_id = Column(GUID, ForeignKey("categorys.id"))
    safety_stock = Column(Integer, default=10)

    # 관계
    category = relationship("Category", back_populates="products")
    transactions = relationship("InventoryTransaction", back_populates="product")
```

---

### 4. `app/schemas/` - Data Layer (Validation)

> API 입출력 데이터 검증 및 변환

**포함 내용:**

- Pydantic 스키마 클래스
- 요청 스키마 (`Create`, `Update`)
- 응답 스키마 (`Response`)
- 공통 스키마 (`Pagination`)

**예시:**

```python
# schemas/product.py
class ProductCreate(BaseModel):
    barcode: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    category_id: UUID
    safety_stock: int = Field(default=10, ge=0)

class ProductResponse(BaseModel):
    id: UUID
    barcode: str
    name: str
    category_id: UUID = Field(alias="categoryId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
```

**Models vs Schemas:**
| 구분 | Models | Schemas |
|------|--------|---------|
| 목적 | DB 테이블 정의 | API 데이터 검증 |
| 라이브러리 | SQLAlchemy | Pydantic |
| 필드명 | snake_case | snake_case (alias로 camelCase 변환) |
| 사용처 | DB 쿼리 | HTTP 요청/응답 |

---

### 5. `app/core/` - Configuration

> 애플리케이션 설정 및 공통 유틸리티

**포함 내용:**

#### `config.py` - 환경 변수

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()  # 싱글톤
```

#### `security.py` - 보안

```python
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

#### `exceptions.py` - 예외

```python
class ApiException(Exception):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message

class NotFoundException(ApiException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(404, "NOT_FOUND", message)
```

---

### 6. `app/db/` - Database Infrastructure

> 데이터베이스 연결 및 설정

**포함 내용:**

#### `base.py` - Base 클래스

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    # 모든 모델이 상속
    pass
```

#### `session.py` - 세션 관리

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

#### `types.py` - 커스텀 타입

```python
class GUID(TypeDecorator):
    """PostgreSQL/SQLite 호환 UUID 타입"""
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return PGUUID(as_uuid=True)
        return CHAR(32)
```

---

## 🔄 데이터 흐름

```
HTTP Request
    ↓
┌─────────────────┐
│  API Router     │  ← Pydantic 스키마로 요청 검증
│  (api/v1/)      │
└────────┬────────┘
         ↓
┌─────────────────┐
│   Service       │  ← 비즈니스 로직 처리
│  (services/)    │
└────────┬────────┘
         ↓
┌─────────────────┐
│   Models        │  ← DB 조작 (SQLAlchemy)
│  (models/)      │
└────────┬────────┘
         ↓
    PostgreSQL
```

---

## 요약

| 폴더        | 레이어         | 책임              |
| ----------- | -------------- | ----------------- |
| `api/`      | Presentation   | HTTP 처리, 라우팅 |
| `services/` | Business       | 비즈니스 로직     |
| `models/`   | Data           | DB 테이블 정의    |
| `schemas/`  | Data           | API 데이터 검증   |
| `core/`     | Configuration  | 설정, 보안, 예외  |
| `db/`       | Infrastructure | DB 연결, 세션     |

---

> **이전**: [1. 기술 스택 개요](./01_tech_stack.md) | **다음**: [3. 비동기 프로그래밍](./03_async_programming.md)
