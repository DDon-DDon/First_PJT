# 4. SQLAlchemy 2.0 가이드

이 문서에서는 **SQLAlchemy 2.0**의 핵심 개념과 프로젝트에서의 사용법을 설명합니다.

---

## 📌 SQLAlchemy란?

SQLAlchemy는 Python의 **ORM(Object-Relational Mapping)** 라이브러리입니다.

### ORM이란?

```
┌──────────────────┐           ┌──────────────────┐
│   Python 객체     │ ←──ORM──→ │   DB 테이블       │
│   class User     │           │   users          │
│   id, name, ...  │           │   id, name, ...  │
└──────────────────┘           └──────────────────┘
```

- **SQL을 직접 작성하지 않고** Python 객체로 DB 조작
- 데이터베이스 독립성 (PostgreSQL ↔ SQLite 전환 용이)
- 타입 안전성과 IDE 자동완성

### 2.0 vs 1.x

| 특징        | 1.x               | 2.0             |
| ----------- | ----------------- | --------------- |
| 쿼리 API    | `session.query()` | `select()`      |
| 비동기      | 부분 지원         | 네이티브 지원   |
| 타입 힌트   | 미지원            | `Mapped[]` 지원 |
| 암묵적 동작 | 많음              | 명시적          |

---

## 🏗️ 기본 구성요소

### 1. Engine (엔진)

DB 연결 풀을 관리하는 **핵심 객체**입니다.

```python
from sqlalchemy.ext.asyncio import create_async_engine

# 비동기 엔진 생성
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/database",
    echo=True,         # SQL 로깅
    pool_size=5,       # 연결 풀 크기
    max_overflow=10    # 추가 연결 허용 수
)
```

### 2. Session (세션)

DB와의 **작업 단위**를 관리합니다.

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False  # 커밋 후에도 객체 접근 가능
)

# 세션 사용
async with AsyncSessionLocal() as session:
    # DB 작업
    pass
```

### 3. Base (베이스)

모든 모델이 상속받는 **기본 클래스**입니다.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

---

## 📝 모델 정의

### 기본 문법

```python
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"  # 테이블 이름

    # 컬럼 정의
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    barcode = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(GUID, ForeignKey("categorys.id"), nullable=False)
    safety_stock = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)

    # 관계 정의
    category = relationship("Category", back_populates="products")
```

### 컬럼 속성

| 속성             | 설명           | 예시                           |
| ---------------- | -------------- | ------------------------------ |
| `primary_key`    | 기본키         | `primary_key=True`             |
| `nullable`       | NULL 허용      | `nullable=False`               |
| `unique`         | 유니크 제약    | `unique=True`                  |
| `index`          | 인덱스 생성    | `index=True`                   |
| `default`        | 기본값         | `default=10`                   |
| `server_default` | DB 레벨 기본값 | `server_default=text("NOW()")` |

### Mapped[] 타입 힌트 (2.0 스타일)

```python
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    barcode: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(default=True)
```

> 프로젝트에서는 Column() 스타일을 주로 사용합니다.

---

## 🔗 관계 정의 (Relationships)

### 1:N (일대다)

```python
class Category(Base):
    __tablename__ = "categorys"

    id = Column(GUID, primary_key=True)
    name = Column(String(50))

    # 일대다: 카테고리 하나에 여러 제품
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    category_id = Column(GUID, ForeignKey("categorys.id"))

    # 다대일: 제품은 하나의 카테고리에 속함
    category = relationship("Category", back_populates="products")
```

### N:M (다대다)

```python
# 중간 테이블
class UserStore(Base):
    __tablename__ = "user_stores"

    user_id = Column(GUID, ForeignKey("users.id"), primary_key=True)
    store_id = Column(GUID, ForeignKey("stores.id"), primary_key=True)
    assigned_at = Column(DateTime, default=func.now())

class User(Base):
    stores = relationship(
        "Store",
        secondary="user_stores",  # 중간 테이블
        back_populates="users"
    )

class Store(Base):
    users = relationship(
        "User",
        secondary="user_stores",
        back_populates="stores"
    )
```

### 로딩 전략

| 전략              | 설명                       | 사용 시점               |
| ----------------- | -------------------------- | ----------------------- |
| `lazy="select"`   | 접근 시 별도 쿼리 (기본값) | 거의 사용 안 함         |
| `lazy="joined"`   | 항상 JOIN                  | 1:1 또는 자주 함께 조회 |
| `lazy="selectin"` | IN 쿼리로 일괄 로드        | 1:N 컬렉션              |

```python
# relationship에서 설정
category = relationship("Category", lazy="joined")

# 쿼리에서 동적 설정
from sqlalchemy.orm import joinedload, selectinload

result = await db.execute(
    select(Product)
    .options(joinedload(Product.category))
)
```

---

## 🔍 쿼리 작성

### SELECT (조회)

```python
from sqlalchemy import select

# 전체 조회
result = await db.execute(select(Product))
products = result.scalars().all()

# 조건 조회
result = await db.execute(
    select(Product).where(Product.barcode == "123")
)
product = result.scalar_one_or_none()  # 없으면 None

# 여러 조건
result = await db.execute(
    select(Product)
    .where(Product.is_active == True)
    .where(Product.category_id == category_id)
)
```

### scalars() 이해하기

```python
result = await db.execute(select(Product))

# Row 객체 반환
rows = result.all()  # [(<Product>,), (<Product>,), ...]

# 스칼라 값 반환
products = result.scalars().all()  # [<Product>, <Product>, ...]
```

### 필터링 메서드

```python
from sqlalchemy import select, and_, or_

# AND 조건
select(Product).where(
    and_(
        Product.is_active == True,
        Product.safety_stock > 0
    )
)

# OR 조건
select(Product).where(
    or_(
        Product.barcode.ilike("%test%"),
        Product.name.ilike("%test%")
    )
)

# LIKE (대소문자 구분)
select(Product).where(Product.name.like("%크림%"))

# ILIKE (대소문자 무시)
select(Product).where(Product.name.ilike("%cream%"))
```

### 정렬, 페이징

```python
# 정렬
select(Product).order_by(Product.created_at.desc())

# 페이징
select(Product).offset(0).limit(20)  # 첫 20개
select(Product).offset(20).limit(20)  # 다음 20개
```

### COUNT

```python
from sqlalchemy import func

# 전체 개수
result = await db.execute(select(func.count(Product.id)))
total = result.scalar()
```

### JOIN

```python
# 명시적 JOIN
result = await db.execute(
    select(Product, Category)
    .join(Category, Product.category_id == Category.id)
)

# relationship 기반 (권장)
result = await db.execute(
    select(Product)
    .options(joinedload(Product.category))
)
```

---

## ✏️ 데이터 조작

### INSERT

```python
# 단건 삽입
product = Product(barcode="123", name="테스트 제품")
db.add(product)
await db.commit()

# 벌크 삽입
products = [Product(...), Product(...), ...]
db.add_all(products)
await db.commit()
```

### UPDATE

```python
# 객체를 통한 업데이트
product = await db.get(Product, product_id)
product.name = "새 이름"
await db.commit()

# 벌크 업데이트
from sqlalchemy import update

await db.execute(
    update(Product)
    .where(Product.category_id == old_category_id)
    .values(category_id=new_category_id)
)
await db.commit()
```

### DELETE

```python
# 객체 삭제
product = await db.get(Product, product_id)
await db.delete(product)
await db.commit()

# 벌크 삭제
from sqlalchemy import delete

await db.execute(
    delete(Product).where(Product.is_active == False)
)
await db.commit()
```

---

## 🔐 트랜잭션

### 기본 트랜잭션

```python
async with db.begin():  # 트랜잭션 시작
    product = Product(...)
    db.add(product)

    stock = CurrentStock(...)
    db.add(stock)
# 자동 커밋 (예외 시 자동 롤백)
```

### 명시적 커밋/롤백

```python
try:
    product = Product(...)
    db.add(product)
    await db.commit()  # 명시적 커밋
except Exception:
    await db.rollback()  # 명시적 롤백
    raise
```

### Nested 트랜잭션 (Savepoint)

```python
async with db.begin():  # 외부 트랜잭션
    db.add(product1)

    async with db.begin_nested():  # Savepoint
        db.add(product2)
        # 실패해도 product1은 유지됨
```

---

## ⚠️ 프로젝트 특수 사항

### GUID 커스텀 타입

프로젝트에서는 PostgreSQL/SQLite 호환을 위해 **GUID** 타입을 사용합니다.

```python
from app.db.types import GUID

class Product(Base):
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    category_id = Column(GUID, ForeignKey("categorys.id"))
```

### 자동 테이블명

`Base` 클래스에서 `__tablename__`을 자동 생성합니다.

```python
# Product → 'products'
# Category → 'categorys'
# InventoryTransaction → 'inventorytransactions'
```

> 복잡한 이름은 수동 지정을 권장합니다.

### relationship에서 comment 사용 금지

```python
# ❌ 에러 발생
category = relationship("Category", comment="카테고리")

# ✅ 올바른 사용
category = relationship("Category")  # 주석은 docstring으로
```

---

## 요약

| 개념           | 설명                     |
| -------------- | ------------------------ |
| Engine         | DB 연결 풀 관리          |
| Session        | 작업 단위 (Unit of Work) |
| Model          | DB 테이블의 Python 표현  |
| select()       | 조회 쿼리 빌더           |
| relationship() | 모델 간 관계 정의        |
| joinedload()   | 관계 데이터 선 로딩      |

---

> **이전**: [3. 비동기 프로그래밍](./03_async_programming.md) | **다음**: [5. Pydantic 가이드](./05_pydantic_guide.md)
