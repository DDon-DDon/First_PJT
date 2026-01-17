# 5. Pydantic V2 가이드

이 문서에서는 **Pydantic V2**의 핵심 개념과 프로젝트에서의 사용 패턴을 설명합니다.

---

## 📌 Pydantic이란?

Pydantic은 **데이터 검증(Validation)** 및 **직렬화(Serialization)** 라이브러리입니다.

### 핵심 기능

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# 자동 검증
user = User(name="김철수", age=25, email="kim@example.com")  # ✅ 성공

user = User(name="김철수", age="스물다섯", email="invalid")  # ❌ 에러
# ValidationError: age: Input should be a valid integer
```

### V2의 장점

| 특징            | 설명                                |
| --------------- | ----------------------------------- |
| **성능**        | Rust 기반 코어, V1 대비 5~50배 빠름 |
| **명확한 API**  | `model_validate()`, `model_dump()`  |
| **Strict 모드** | 타입 강제 변환 비활성화 옵션        |

---

## 🏗️ 기본 사용법

### 1. 모델 정의

```python
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProductBase(BaseModel):
    barcode: str
    name: str
    category_id: UUID

class ProductCreate(ProductBase):
    safety_stock: int = 10  # 기본값

class ProductResponse(ProductBase):
    id: UUID
    is_active: bool
```

### 2. 데이터 검증

```python
# 딕셔너리 → 모델
data = {"barcode": "123", "name": "테스트", "category_id": "...uuid..."}
product = ProductCreate.model_validate(data)

# JSON 문자열 → 모델
json_str = '{"barcode": "123", "name": "테스트", ...}'
product = ProductCreate.model_validate_json(json_str)
```

### 3. 직렬화

```python
# 모델 → 딕셔너리
data = product.model_dump()

# 모델 → JSON 문자열
json_str = product.model_dump_json()

# 특정 필드만
data = product.model_dump(include={"barcode", "name"})
data = product.model_dump(exclude={"id"})
```

---

## ✅ Field 검증

### 기본 검증

```python
from pydantic import Field

class ProductCreate(BaseModel):
    barcode: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., max_length=200)
    safety_stock: int = Field(default=10, ge=0, le=10000)
    # ge: greater than or equal (이상)
    # le: less than or equal (이하)
```

### Field 옵션

| 옵션             | 설명      | 예시                         |
| ---------------- | --------- | ---------------------------- |
| `...` (Ellipsis) | 필수 필드 | `Field(...)`                 |
| `default`        | 기본값    | `Field(default=10)`          |
| `min_length`     | 최소 길이 | `Field(min_length=1)`        |
| `max_length`     | 최대 길이 | `Field(max_length=50)`       |
| `ge`             | >=        | `Field(ge=0)`                |
| `le`             | <=        | `Field(le=100)`              |
| `gt`             | >         | `Field(gt=0)`                |
| `lt`             | <         | `Field(lt=100)`              |
| `pattern`        | 정규식    | `Field(pattern=r"^\d{13}$")` |
| `alias`          | 필드 별칭 | `Field(alias="safetyStock")` |

### 커스텀 검증

```python
from pydantic import field_validator

class ProductCreate(BaseModel):
    barcode: str

    @field_validator("barcode")
    @classmethod
    def validate_barcode(cls, v: str) -> str:
        if not v.isdigit() and not v.startswith("DON-"):
            raise ValueError("바코드는 숫자 또는 DON-으로 시작해야 합니다")
        return v
```

### 모델 레벨 검증

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "DateRange":
        if self.end_date < self.start_date:
            raise ValueError("종료일은 시작일 이후여야 합니다")
        return self
```

---

## 🔄 ORM 통합 (from_attributes)

### SQLAlchemy 모델 → Pydantic 스키마

```python
from pydantic import ConfigDict

class ProductResponse(BaseModel):
    id: UUID
    barcode: str
    name: str

    model_config = ConfigDict(from_attributes=True)

# 사용
product_orm = await db.get(Product, id)  # SQLAlchemy 객체
response = ProductResponse.model_validate(product_orm)  # 자동 변환
```

---

## 📝 Alias (snake_case ↔ camelCase)

### 문제 상황

```
Python/DB:  snake_case  (safety_stock, is_active)
JSON API:   camelCase   (safetyStock, isActive)
```

### 해결책 1: 개별 alias 지정 (현재 구현)

```python
class ProductResponse(BaseModel):
    # 필드명: snake_case (ORM과 일치)
    # alias: camelCase (JSON 출력)
    safety_stock: int = Field(..., alias="safetyStock")
    is_active: bool = Field(..., alias="isActive")
    category_id: UUID = Field(..., alias="categoryId")

    model_config = ConfigDict(
        from_attributes=True,      # ORM 변환 허용
        populate_by_name=True      # 필드명/alias 모두 허용
    )
```

### 해결책 2: alias_generator 사용 (예정 구현 🚧)

> [!NOTE]
> 이 방법은 아직 프로젝트에 적용되지 않았지만, 향후 개선을 위해 권장됩니다.

모든 필드에 자동으로 alias를 적용할 수 있습니다.

```python
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

class ProductResponse(BaseModel):
    # 필드명: snake_case로만 정의
    safety_stock: int
    is_active: bool
    category_id: UUID
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel  # 자동으로 camelCase 변환!
    )

# 결과:
# safety_stock → safetyStock
# is_active → isActive
# category_id → categoryId
# created_at → createdAt
```

**장점:**

- 필드가 많을 때 코드가 훨씬 간결
- 일관된 네이밍 규칙 자동 적용
- 실수 방지 (오타 가능성 제거)

**언제 개별 alias를 사용?**

- 특정 필드만 다른 이름으로 변환해야 할 때
- 레거시 API 호환성 유지 시

**혼합 사용 예시:**

```python
class ProductResponse(BaseModel):
    safety_stock: int  # → safetyStock (자동)
    is_active: bool    # → isActive (자동)

    # 특정 필드만 수동 지정
    category_id: UUID = Field(alias="catId")  # → catId

    model_config = ConfigDict(
        alias_generator=to_camel
    )
```

### 동작 방식

```python
# ORM → Pydantic (from_attributes)
product = ProductResponse.model_validate(orm_product)

# JSON 직렬화 (alias 사용)
json_str = product.model_dump_json(by_alias=True)
# {"safetyStock": 10, "isActive": true, "categoryId": "..."}

# JSON 역직렬화 (alias 허용)
data = {"safetyStock": 10, "isActive": True}
product = ProductResponse.model_validate(data)  # ✅ 성공

# 필드명도 허용 (populate_by_name=True)
data = {"safety_stock": 10, "is_active": True}
product = ProductResponse.model_validate(data)  # ✅ 성공
```

---

## 📦 프로젝트 스키마 구조

### 파일 구조

```
app/schemas/
├── common.py      # 공통 스키마 (페이지네이션, 응답 래퍼)
├── product.py     # 제품 관련
├── transaction.py # 트랜잭션 관련
├── sync.py        # 동기화 관련
├── inventory.py   # 재고 관련
└── user.py        # 사용자 관련
```

### 네이밍 컨벤션

```python
# Base: 공통 필드
class ProductBase(BaseModel):
    barcode: str
    name: str

# Create: 생성 요청
class ProductCreate(ProductBase):
    safety_stock: int = 10

# Update: 수정 요청 (모든 필드 Optional)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    safety_stock: Optional[int] = None

# Response: API 응답
class ProductResponse(ProductBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# Filter: 쿼리 파라미터
class ProductFilter(BaseModel):
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None
```

---

## 🎯 실제 사용 예시

### API 요청 검증

```python
# app/api/v1/products.py
from app.schemas.product import ProductCreate, ProductResponse

@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,  # 자동 검증
    db: AsyncSession = Depends(get_db)
):
    # data는 이미 검증된 ProductCreate 객체
    return await product_service.create(db, data)
```

### 서비스에서 사용

```python
# app/services/product.py
async def create(db: AsyncSession, data: ProductCreate) -> Product:
    # Pydantic → dict → ORM
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    return product
```

### 응답 변환

```python
# 단일 객체
product = await db.get(Product, id)
return ProductResponse.model_validate(product)

# 목록
products = result.scalars().all()
return [ProductResponse.model_validate(p) for p in products]
```

---

## ⚠️ 주의사항

### 1. model_config 설정 누락

```python
# ❌ ORM 변환 실패
class ProductResponse(BaseModel):
    id: UUID
    name: str
    # model_config 누락

ProductResponse.model_validate(orm_product)
# ValidationError: Input should be a valid dictionary

# ✅ 올바른 설정
class ProductResponse(BaseModel):
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)
```

### 2. alias 불일치

```python
# ❌ ORM 속성과 스키마 필드명 불일치
class ProductResponse(BaseModel):
    safetyStock: int  # ORM에는 safety_stock

ProductResponse.model_validate(orm_product)
# ValidationError: Field required

# ✅ alias 사용
class ProductResponse(BaseModel):
    safety_stock: int = Field(alias="safetyStock")
```

### 3. Optional 필드 기본값

```python
# ❌ Optional인데 기본값 없음
class Filter(BaseModel):
    category_id: Optional[UUID]  # 기본값 None 필요

# ✅ 올바른 정의
class Filter(BaseModel):
    category_id: Optional[UUID] = None
    # 또는
    category_id: UUID | None = None
```

---

## 요약

| 개념               | 설명                      |
| ------------------ | ------------------------- |
| `BaseModel`        | 스키마 기본 클래스        |
| `Field()`          | 필드 검증 규칙            |
| `model_validate()` | 데이터 → 모델 변환        |
| `model_dump()`     | 모델 → dict 변환          |
| `from_attributes`  | ORM 객체 변환 허용        |
| `alias`            | 필드 별칭 (camelCase)     |
| `alias_generator`  | 자동 alias 변환 (🚧 예정) |
| `populate_by_name` | 필드명/alias 모두 허용    |

---

> **이전**: [4. SQLAlchemy 가이드](./04_sqlalchemy_guide.md) | **다음**: [6. FastAPI 가이드](./06_fastapi_guide.md)
