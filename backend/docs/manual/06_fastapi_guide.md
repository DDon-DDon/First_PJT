# 6. FastAPI 가이드

이 문서에서는 **FastAPI**의 핵심 개념과 프로젝트에서의 활용법을 설명합니다.

---

## 📌 FastAPI란?

FastAPI는 **현대적인 Python 웹 API 프레임워크**입니다.

### 특징

| 특징            | 설명                                        |
| --------------- | ------------------------------------------- |
| **고성능**      | Starlette + Uvicorn 기반, Node.js/Go급 성능 |
| **자동 문서화** | Swagger UI, ReDoc 자동 생성                 |
| **타입 검증**   | Pydantic 통합으로 런타임 검증               |
| **비동기**      | async/await 네이티브 지원                   |
| **의존성 주입** | 내장 DI 시스템                              |

---

## 🚀 기본 구조

### 앱 생성

```python
# app/main.py
from fastapi import FastAPI
from app.api.v1 import products, inventory, transactions

app = FastAPI(
    title="DDon-DDon API",
    description="재고 관리 시스템 API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(inventory.router, prefix="/api/v1", tags=["inventory"])
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])
```

### 라우터 정의

```python
# app/api/v1/products.py
from fastapi import APIRouter

router = APIRouter(prefix="/products")

@router.get("/")
async def list_products():
    ...

@router.get("/{product_id}")
async def get_product(product_id: UUID):
    ...

@router.post("/")
async def create_product():
    ...
```

---

## 🛣️ 경로 연산 (Path Operations)

### HTTP 메서드

```python
@router.get("/items")          # 조회 (목록)
@router.get("/items/{id}")     # 조회 (단건)
@router.post("/items")         # 생성
@router.put("/items/{id}")     # 전체 수정
@router.patch("/items/{id}")   # 부분 수정
@router.delete("/items/{id}")  # 삭제
```

### 경로 파라미터 (Path Parameters)

URL 경로의 일부를 변수로 받습니다.

```python
@router.get("/products/{product_id}")
async def get_product(product_id: UUID):  # 자동 타입 변환
    return await db.get(Product, product_id)

# /products/123e4567-e89b-12d3-a456-426614174000
# → product_id = UUID("123e4567-e89b-12d3-a456-426614174000")
```

### 쿼리 파라미터 (Query Parameters)

URL `?key=value` 형식으로 받습니다.

```python
@router.get("/products")
async def list_products(
    page: int = 1,                    # 기본값 있음 = 선택적
    limit: int = 20,
    search: str | None = None,        # None 허용 = 선택적
    category_id: UUID | None = None
):
    ...

# /products?page=2&limit=10&search=크림
```

### Query 객체 검증

```python
from fastapi import Query

@router.get("/products")
async def list_products(
    page: int = Query(default=1, ge=1, description="페이지 번호"),
    limit: int = Query(default=20, ge=1, le=100, description="페이지당 개수"),
    search: str | None = Query(default=None, max_length=100)
):
    ...
```

### 요청 본문 (Request Body)

Pydantic 모델로 JSON 본문을 받습니다.

```python
from app.schemas.product import ProductCreate

@router.post("/products")
async def create_product(data: ProductCreate):  # 자동 검증
    # data는 검증된 ProductCreate 객체
    return await product_service.create(db, data)
```

---

## 🔌 의존성 주입 (Dependency Injection)

### 개념

```python
from fastapi import Depends

def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db  # 요청 처리 중 사용
    finally:
        db.close()  # 요청 종료 시 정리

@router.get("/products")
async def list_products(db: Session = Depends(get_db)):
    # db가 자동으로 주입됨
    return db.query(Product).all()
```

### 장점

1. **코드 재사용**: 공통 로직을 의존성으로 분리
2. **테스트 용이**: 의존성을 모킹으로 교체 가능
3. **관심사 분리**: 라우터는 비즈니스 로직에만 집중

### 프로젝트 의존성

```python
# app/api/deps.py

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """비동기 DB 세션"""
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """현재 인증된 사용자"""
    payload = jwt.decode(token, SECRET_KEY)
    user = await db.get(User, payload["sub"])
    if not user:
        raise UnauthorizedException()
    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    """관리자 권한 필수"""
    if user.role != "ADMIN":
        raise ForbiddenException()
    return user
```

### 사용 예시

```python
@router.get("/products")
async def list_products(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)  # 인증 필수
):
    ...

@router.post("/products")
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)  # 관리자만
):
    ...
```

---

## 📤 응답 처리

### response_model

응답 데이터를 Pydantic 모델로 직렬화합니다.

```python
@router.get("/products/{id}", response_model=ProductResponse)
async def get_product(id: UUID, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, id)
    return product  # 자동으로 ProductResponse로 변환
```

### 상태 코드

```python
from fastapi import status

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product():
    ...

@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product():
    ...
```

### 목록 응답 패턴

```python
class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    pagination: PaginationMeta

@router.get("/products", response_model=ProductListResponse)
async def list_products(page: int = 1, limit: int = 20):
    products, total = await product_service.list(db, page, limit)
    return {
        "items": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": ceil(total / limit)
        }
    }
```

---

## ⚠️ 예외 처리

### HTTPException

```python
from fastapi import HTTPException

@router.get("/products/{id}")
async def get_product(id: UUID):
    product = await db.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product
```

### 커스텀 예외 헨들러

```python
# app/core/exceptions.py
class ApiException(Exception):
    def __init__(self, status_code: int, error_code: str, message: str, details: dict = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details

class NotFoundException(ApiException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(404, "NOT_FOUND", message)

class InsufficientStockException(ApiException):
    def __init__(self, current: int, requested: int):
        super().__init__(
            400, "INSUFFICIENT_STOCK", "재고가 부족합니다",
            {"current": current, "requested": requested}
        )
```

```python
# app/main.py
from fastapi import Request
from fastapi.responses import JSONResponse

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

---

## 📝 자동 문서화

FastAPI는 OpenAPI 스펙 기반 문서를 자동 생성합니다.

### 접근 URL

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

### 문서 보강

```python
@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="제품 상세 조회",
    description="바코드 또는 제품 ID로 제품 정보를 조회합니다.",
    responses={
        200: {"description": "제품 정보"},
        404: {"description": "제품을 찾을 수 없음"}
    }
)
async def get_product(
    product_id: UUID = Path(..., description="제품 고유 ID")
):
    """
    제품 상세 정보를 반환합니다.

    - **product_id**: UUID 형식의 제품 ID
    """
    ...
```

---

## 🔒 미들웨어

### CORS 설정

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용 도메인
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드
    allow_headers=["*"],  # 모든 헤더
)
```

### 커스텀 미들웨어

```python
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Process-Time"] = str(duration)
        return response

app.add_middleware(TimingMiddleware)
```

---

## 🧪 테스트

### TestClient

```python
from fastapi.testclient import TestClient
from httpx import AsyncClient

# 동기 테스트
def test_sync():
    with TestClient(app) as client:
        response = client.get("/products")
        assert response.status_code == 200

# 비동기 테스트 (권장)
import pytest

@pytest.mark.asyncio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/products")
        assert response.status_code == 200
```

### 의존성 오버라이드

```python
def test_with_mock_db():
    # 테스트용 DB 세션으로 교체
    app.dependency_overrides[get_db] = get_test_db

    # 테스트용 사용자로 교체
    app.dependency_overrides[get_current_user] = lambda: mock_user

    # 테스트 실행
    ...

    # 정리
    app.dependency_overrides.clear()
```

---

## 요약

| 개념                   | 설명           |
| ---------------------- | -------------- |
| `APIRouter`            | 라우터 모듈화  |
| `@router.get/post/...` | 경로 연산 정의 |
| `Path()`, `Query()`    | 파라미터 검증  |
| `Depends()`            | 의존성 주입    |
| `response_model`       | 응답 스키마    |
| `HTTPException`        | 예외 발생      |
| `include_router`       | 라우터 통합    |

---

> **이전**: [5. Pydantic 가이드](./05_pydantic_guide.md) | **다음**: [7. 커스텀 타입과 유틸리티](./07_custom_types.md)
