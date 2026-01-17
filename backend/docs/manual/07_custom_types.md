# 7. 커스텀 타입과 유틸리티

이 문서에서는 프로젝트에서 사용하는 **커스텀 타입**, **예외 처리**, **공통 패턴**을 설명합니다.

---

## 📌 GUID 커스텀 타입

### 문제 상황

| DB         | UUID 지원                 |
| ---------- | ------------------------- |
| PostgreSQL | ✅ 네이티브 UUID 타입     |
| SQLite     | ❌ 미지원 (문자열로 저장) |

프로덕션에서는 PostgreSQL을, 테스트에서는 SQLite를 사용하기 때문에 호환성이 필요합니다.

### 해결책: GUID TypeDecorator

```python
# app/db/types.py

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

class GUID(TypeDecorator):
    """PostgreSQL/SQLite 호환 UUID 타입"""

    impl = CHAR            # 기본 구현체
    cache_ok = True        # 쿼리 캐싱 허용

    def load_dialect_impl(self, dialect):
        """DB별 타입 선택"""
        if dialect.name == 'postgresql':
            # PostgreSQL: 네이티브 UUID
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        else:
            # SQLite 등: CHAR(32)로 저장
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        """Python → DB 저장 시 변환"""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)  # 하이픈 포함
        else:
            return value.hex   # 하이픈 제거 (32자)

    def process_result_value(self, value, dialect):
        """DB → Python 조회 시 변환"""
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value
```

### 사용법

```python
from app.db.types import GUID

class Product(Base):
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    category_id = Column(GUID, ForeignKey("categorys.id"))
```

### 동작 예시

```
PostgreSQL:
  저장: "550e8400-e29b-41d4-a716-446655440000"
  조회: uuid.UUID("550e8400-...")

SQLite:
  저장: "550e8400e29b41d4a716446655440000"
  조회: uuid.UUID("550e8400-...")  # 자동 변환
```

---

## ⚠️ 예외 처리 패턴

### 예외 클래스 구조

```python
# app/core/exceptions.py

class ApiException(Exception):
    """API 예외 기본 클래스"""
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: dict | None = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundException(ApiException):
    """404 Not Found"""
    def __init__(self, message: str = "리소스를 찾을 수 없습니다"):
        super().__init__(404, "NOT_FOUND", message)


class ConflictException(ApiException):
    """409 Conflict (중복)"""
    def __init__(self, message: str = "이미 존재하는 데이터입니다"):
        super().__init__(409, "CONFLICT", message)


class UnauthorizedException(ApiException):
    """401 Unauthorized"""
    def __init__(self, message: str = "인증이 필요합니다"):
        super().__init__(401, "UNAUTHORIZED", message)


class ForbiddenException(ApiException):
    """403 Forbidden"""
    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__(403, "FORBIDDEN", message)


class InsufficientStockException(ApiException):
    """재고 부족"""
    def __init__(self, current: int, requested: int):
        super().__init__(
            400,
            "INSUFFICIENT_STOCK",
            "재고가 부족합니다",
            {"current": current, "requested": requested}
        )
```

### 예외 핸들러 등록

```python
# app/main.py

from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import ApiException

@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
```

### 사용 예시

```python
# 서비스에서 예외 발생
async def process_outbound(db, data, user):
    stock = await get_current_stock(db, data.product_id, data.store_id)

    if stock.quantity < data.quantity:
        raise InsufficientStockException(
            current=stock.quantity,
            requested=data.quantity
        )
    ...

# API 응답 예시
# HTTP 400
{
    "success": false,
    "error": {
        "code": "INSUFFICIENT_STOCK",
        "message": "재고가 부족합니다",
        "details": {
            "current": 5,
            "requested": 10
        }
    }
}
```

---

## 🔧 설정 관리 (Settings)

### pydantic-settings 사용

```python
# app/core/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 데이터베이스
    DATABASE_URL: str

    # 보안
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()  # 싱글톤 패턴
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### .env 파일

```bash
# .env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/donedone
SECRET_KEY=your-super-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 사용법

```python
from app.core.config import settings

# 직접 접근
database_url = settings.DATABASE_URL

# 의존성으로 주입 (테스트 용이)
from fastapi import Depends

def get_settings_dep() -> Settings:
    return settings

@router.get("/config")
async def get_config(settings: Settings = Depends(get_settings_dep)):
    return {"algorithm": settings.ALGORITHM}
```

---

## 🔐 보안 유틸리티

### 비밀번호 해싱

```python
# app/core/security.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain, hashed)
```

### JWT 토큰 생성

```python
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None
) -> str:
    """액세스 토큰 생성"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access"
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
```

---

## 📊 공통 스키마

### 페이지네이션

```python
# app/schemas/common.py

from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    """페이지네이션 요청 파라미터"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

class PaginationMeta(BaseModel):
    """페이지네이션 메타 정보"""
    page: int
    limit: int
    total: int
    total_pages: int
```

### 표준 응답 래퍼

```python
from typing import Generic, TypeVar
from datetime import datetime

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """표준 API 응답"""
    success: bool = True
    data: T
    meta: dict | None = None

class ApiErrorResponse(BaseModel):
    """에러 응답"""
    success: bool = False
    error: dict
```

---

## 📝 공통 패턴

### 서비스 함수 시그니처

```python
async def service_function(
    db: AsyncSession,       # 1. DB 세션
    data: SomeCreateSchema, # 2. 입력 데이터
    user: User | None = None # 3. 현재 사용자 (선택)
) -> SomeModel:
    ...
```

### 에러 처리 패턴

```python
async def get_product(db: AsyncSession, product_id: UUID) -> Product:
    product = await db.get(Product, product_id)
    if not product:
        raise NotFoundException(f"제품을 찾을 수 없습니다: {product_id}")
    return product
```

### N+1 방지

```python
from sqlalchemy.orm import joinedload, selectinload

# 단일 관계 (1:1, N:1)
result = await db.execute(
    select(Product).options(joinedload(Product.category))
)

# 컬렉션 관계 (1:N)
result = await db.execute(
    select(Category).options(selectinload(Category.products))
)
```

---

## 요약

| 유틸리티       | 파일                 | 역할                        |
| -------------- | -------------------- | --------------------------- |
| GUID           | `db/types.py`        | PostgreSQL/SQLite UUID 호환 |
| ApiException   | `core/exceptions.py` | 표준화된 에러 응답          |
| Settings       | `core/config.py`     | 환경 변수 관리              |
| security       | `core/security.py`   | 비밀번호, JWT               |
| common schemas | `schemas/common.py`  | 페이지네이션, 응답 래퍼     |

---

> **이전**: [6. FastAPI 가이드](./06_fastapi_guide.md) | **다음**: [8. 테스트 가이드](./08_testing_guide.md)
