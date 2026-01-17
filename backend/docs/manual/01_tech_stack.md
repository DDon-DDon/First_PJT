# 1. 기술 스택 개요

이 문서에서는 프로젝트에서 사용되는 **핵심 기술 스택**과 각 기술이 **왜 선택되었는지**를 설명합니다.

---

## 📌 기술 스택 요약

```
┌─────────────────────────────────────────────────────────────┐
│                      응용 계층                               │
│   FastAPI (웹 프레임워크) + Pydantic (데이터 검증)           │
├─────────────────────────────────────────────────────────────┤
│                      데이터 계층                             │
│   SQLAlchemy 2.0 (ORM) + asyncpg (비동기 드라이버)          │
├─────────────────────────────────────────────────────────────┤
│                      인프라 계층                             │
│   PostgreSQL (데이터베이스) + Alembic (마이그레이션)         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐍 Python 3.12+

### 개념

Python은 읽기 쉽고 생산성이 높은 범용 프로그래밍 언어입니다.

### 왜 Python 3.12+인가?

1. **네이티브 async/await**: 비동기 I/O를 언어 레벨에서 지원
2. **타입 힌트 강화**: `X | None` 문법, `TypedDict`, `Generic` 개선
3. **성능 향상**: 인터프리터 최적화로 10~30% 속도 향상

### 프로젝트에서의 사용

```python
# Python 3.10+ 유니온 타입 문법
def get_user(user_id: str) -> User | None:
    ...

# 비동기 함수
async def fetch_data() -> dict:
    ...
```

---

## ⚡ FastAPI

### 개념

FastAPI는 **현대적인 Python 웹 API 프레임워크**입니다.
자동 문서화, 타입 검증, 비동기 지원을 기본 제공합니다.

### 왜 FastAPI인가?

| 특징                | 설명                                     |
| ------------------- | ---------------------------------------- |
| **고성능**          | Starlette 기반, Node.js/Go와 동등한 성능 |
| **자동 문서화**     | Swagger UI, ReDoc 자동 생성              |
| **타입 안전**       | Pydantic 통합으로 런타임 검증            |
| **비동기 네이티브** | async/await 완벽 지원                    |

### 핵심 개념

#### 1) 경로 연산 (Path Operations)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")  # HTTP 메서드 + 경로
async def read_item(item_id: int):  # 경로 파라미터 자동 타입 변환
    return {"item_id": item_id}
```

#### 2) 의존성 주입 (Dependency Injection)

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):  # 자동 주입
    return db.query(User).all() # db.query(User).all() : User 모델의 모든 데이터를 가져온다.
```

### 프로젝트에서의 위치

```
app/
├── main.py       # FastAPI 앱 인스턴스
└── api/
    └── v1/       # 버전별 라우터
        ├── products.py
        ├── inventory.py
        └── transactions.py
```

---

## 🗄️ SQLAlchemy 2.0

### 개념

SQLAlchemy는 Python의 **ORM(Object-Relational Mapping)** 라이브러리입니다.
SQL 쿼리를 Python 객체로 조작할 수 있게 해줍니다.

### 왜 SQLAlchemy 2.0인가?

1. **비동기 지원**: `async_session` 네이티브 지원
2. **타입 힌트**: `Mapped[]`, `mapped_column()` 문법
3. **명확한 실행**: 1.x의 암묵적 동작 제거

### 핵심 개념

#### 1) ORM 모델 정의

```python
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True) # primary_key=True : 기본 키
    name: Mapped[str] = mapped_column(String(100)) # String(100) : 문자열 타입, 최대 100자
    email: Mapped[str] = mapped_column(String(255), unique=True) # unique=True : 중복 키
```

> **Mapped[]**: 컬럼의 Python 타입을 명시
> **mapped_column()**: 컬럼 속성 정의

#### 2) 관계 정의 (Relationships)

```python
class Product(Base):
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # 다대일 관계 : 여러 제품은 하나의 카테고리에 속할 수 있다.
    category: Mapped["Category"] = relationship(back_populates="products")

class Category(Base):
    # 일대다 관계 : 하나의 카테고리는 여러 제품을 가질 수 있다.
    products: Mapped[list["Product"]] = relationship(back_populates="category")
```

#### 3) 비동기 쿼리

```python
from sqlalchemy import select # select문을 사용하기 위한 모듈
from sqlalchemy.ext.asyncio import AsyncSession # 비동기 세션을 사용하기 위한 모듈

async def get_products(db: AsyncSession) -> list[Product]: # 비동기 함수로 정의 : async/await를 사용하여 비동기적으로 데이터를 가져올 수 있다.
    result = await db.execute(select(Product)) # select문을 사용하여 데이터를 가져온다.
    return result.scalars().all() # scalars() : 스칼라는 fastapi에서 사용되는 타입으로 변환한다. (Product 모델의 타입을 반환) all() : 결과를 리스트로 반환한다.
```

### 프로젝트에서의 위치

```
app/
├── db/
│   ├── base.py      # Base 클래스 정의
│   ├── session.py   # 세션 팩토리
│   └── types.py     # 커스텀 타입 (GUID)
└── models/
    ├── user.py
    ├── product.py
    └── transaction.py
```

---

## ✅ Pydantic V2

### 개념

Pydantic은 **데이터 검증 및 직렬화** 라이브러리입니다.
타입 힌트를 사용하여 런타임에 데이터를 검증합니다.

### 왜 Pydantic인가?

1. **타입 기반 검증**: 타입 힌트만으로 자동 검증
2. **성능**: Rust 기반 코어로 V1 대비 5~50배 빠름
3. **FastAPI 통합**: 요청/응답 자동 변환

### 핵심 개념

#### 1) 스키마 정의

```python
from pydantic import BaseModel, Field # BaseModel : 스키마를 정의하기 위한 모듈 Field : 필드를 정의하기 위한 모듈

class ProductCreate(BaseModel): # ProductCreate : 제품 생성을 위한 스키마
    barcode: str = Field(..., min_length=1, max_length=50) # min_length=1, max_length=50 : barcode의 최소 길이와 최대 길이
    name: str = Field(..., max_length=200) # max_length=200 : name의 최대 길이
    safety_stock: int = Field(default=10, ge=0) # default=10 : 기본값, ge=0 : 0 이상
```

#### 2) ORM 모델 변환

```python
from pydantic import ConfigDict

class ProductResponse(BaseModel): # ProductResponse : 제품 응답을 위한 스키마
    id: UUID # UUID : UUID 타입 -> GUID 타입으로 변경됨
    barcode: str # barcode : barcode
    name: str # name : name

    model_config = ConfigDict(from_attributes=True)  # ORM → Pydantic : ORM에서 Pydantic으로 변환

# 사용
product = db.query(Product).first() # Product 모델에서 첫 번째 데이터를 가져온다. (ORM)
response = ProductResponse.model_validate(product)  # ProductResponse 스키마로 변환 (model_validate: Pydantic의 메소드인데 ORM에서 Pydantic으로 변환하는 역할)
```

#### 3) Alias (snake_case ↔ camelCase)

```python
class ProductResponse(BaseModel):
    safety_stock: int = Field(alias="safetyStock") # alias : 필드명을 변환하기 위한 모듈
    is_active: bool = Field(alias="isActive")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # 필드명/alias 모두 허용
    )
```

### 프로젝트에서의 위치

```
app/
└── schemas/
    ├── common.py      # 공통 스키마 (Pagination)
    ├── product.py     # 제품 스키마
    ├── transaction.py # 트랜잭션 스키마
    └── sync.py        # 동기화 스키마
```

---

## 🔄 asyncpg

### 개념

asyncpg는 PostgreSQL용 **순수 비동기 드라이버**입니다.
libpq(C 라이브러리) 대신 순수 Python/Cython으로 구현되어 있습니다.

### 왜 asyncpg인가?

1. **성능**: psycopg2보다 3배 이상 빠름
2. **네이티브 비동기**: async/await 완벽 지원
3. **PostgreSQL 특화**: JSONB, Array 등 고급 타입 지원

### 연결 문자열

```python
# SQLAlchemy + asyncpg 조합
DATABASE_URL = "postgresql+asyncpg://user:password@host:5432/database"
```

---

## 📦 Alembic

### 개념

Alembic은 SQLAlchemy용 **데이터베이스 마이그레이션** 도구입니다.
스키마 변경사항을 버전 관리하고 적용합니다.

### 핵심 명령어

```bash
# 마이그레이션 파일 자동 생성
alembic revision --autogenerate -m "Add product table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

### 프로젝트에서의 위치

```
backend/
├── alembic/
│   ├── versions/     # 마이그레이션 파일들
│   └── env.py        # Alembic 설정
└── alembic.ini       # 설정 파일
```

---

## 요약

| 기술           | 역할          | 특징                     |
| -------------- | ------------- | ------------------------ |
| Python 3.12    | 런타임        | 타입 힌트, async/await   |
| FastAPI        | 웹 프레임워크 | 자동 문서화, 의존성 주입 |
| SQLAlchemy 2.0 | ORM           | 비동기, 타입 안전        |
| Pydantic V2    | 데이터 검증   | 고성능, 자동 변환        |
| asyncpg        | DB 드라이버   | 순수 비동기              |
| Alembic        | 마이그레이션  | 스키마 버전 관리         |

---

> **이전**: [목차](./00_index.md) | **다음**: [2. 프로젝트 구조](./02_project_structure.md)
