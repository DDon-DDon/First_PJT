# DoneDone 백엔드 고도화 로드맵

**작성일**: 2026-01-24  
**목적**: MVP 완성 후 프로덕션 레벨 백엔드로 발전시키기 위한 단계별 가이드  
**예상 기간**: 4-6주 (파트타임 기준)

---

## 📋 전체 진행 체크리스트

```
Phase A: API 문서화 & DX          ████████████████████ 100%  ✅
Phase B: 테스트 강화              ████████████████████ 100%  ✅
Phase C: 에러 핸들링 & 로깅       ████████████████████ 100%  ✅
Phase D: 쿼리 최적화 & 벤치마크   ░░░░░░░░░░░░░░░░░░░░   0%
Phase E: 인프라 & 배포            ░░░░░░░░░░░░░░░░░░░░   0%
Phase F: 보안 강화                ░░░░░░░░░░░░░░░░░░░░   0%
```

---

## Phase A: API 문서화 & DX (Developer Experience)

**목표**: 프론트엔드 개발자가 별도 설명 없이 API를 사용할 수 있도록 함  
**예상 기간**: 3-4일

### A-1. OpenAPI 스펙 강화 ✅

#### 체크리스트

- [x] 모든 엔드포인트에 `summary`, `description` 추가
- [x] 요청/응답 예시(examples) 추가
- [x] 에러 응답 스키마 정의 (`responses` 파라미터)
- [x] 태그(tags)로 API 그룹화

#### 구현 가이드

**1) 공통 에러 응답 스키마 정의**

```python
# app/schemas/common.py
from pydantic import BaseModel
from typing import Optional, Any

class ErrorResponse(BaseModel):
    """API 에러 응답 공통 스키마"""
    error_code: str
    message: str
    detail: Optional[Any] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error_code": "PRODUCT_NOT_FOUND",
                    "message": "해당 바코드의 제품을 찾을 수 없습니다",
                    "detail": {"barcode": "8801234567890"}
                }
            ]
        }
    }

class PaginatedResponse(BaseModel):
    """페이지네이션 공통 응답"""
    items: list
    total: int
    page: int
    size: int
    has_next: bool
```

**2) 엔드포인트별 문서화 예시**

```python
# app/api/v1/products.py
from fastapi import APIRouter, Query, Path
from app.schemas.common import ErrorResponse

router = APIRouter(prefix="/products", tags=["제품 관리"])

@router.get(
    "/barcode/{barcode}",
    response_model=ProductResponse,
    summary="바코드로 제품 조회",
    description="""
    POS 또는 모바일에서 바코드 스캔 시 호출하는 API입니다.

    - 바코드 인덱스를 활용하여 100ms 이내 응답을 보장합니다.
    - 제품이 없는 경우 404를 반환합니다.
    """,
    responses={
        200: {
            "description": "제품 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "barcode": "8801234567890",
                        "name": "새우깡",
                        "category": {"id": "...", "name": "스낵"},
                        "unit": "봉",
                        "price": 1500
                    }
                }
            }
        },
        404: {
            "model": ErrorResponse,
            "description": "제품을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "PRODUCT_NOT_FOUND",
                        "message": "해당 바코드의 제품을 찾을 수 없습니다"
                    }
                }
            }
        }
    }
)
async def get_product_by_barcode(
    barcode: str = Path(
        ...,
        description="제품 바코드 (EAN-13 형식)",
        example="8801234567890",
        min_length=8,
        max_length=14
    )
):
    ...
```

**3) Query 파라미터 문서화**

```python
@router.get(
    "/",
    response_model=PaginatedResponse[ProductResponse],
    summary="제품 목록 조회",
    description="검색, 카테고리 필터링, 페이지네이션을 지원하는 제품 목록 API"
)
async def list_products(
    q: Optional[str] = Query(
        None,
        description="제품명 또는 바코드 검색어",
        example="새우깡",
        max_length=100
    ),
    category_id: Optional[UUID] = Query(
        None,
        description="카테고리 ID로 필터링"
    ),
    page: int = Query(
        1,
        ge=1,
        description="페이지 번호 (1부터 시작)"
    ),
    size: int = Query(
        20,
        ge=1,
        le=100,
        description="페이지당 항목 수 (최대 100)"
    )
):
    ...
```

### A-2. API 문서 커스터마이징 ✅

#### 체크리스트

- [x] Swagger UI 타이틀, 설명 커스터마이징
- [x] API 버전 정보 표시
- [x] 서버 URL 환경별 구분

#### 구현 가이드

```python
# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="DoneDone API",
    description="""
    ## 똔똔 재고관리 시스템 API

    오프라인 매장을 위한 바코드 기반 재고관리 API입니다.

    ### 주요 기능
    - 🔍 **제품 관리**: 바코드 조회, 제품 등록/수정
    - 📦 **재고 관리**: 입고, 출고, 재고 조정
    - 🔄 **오프라인 동기화**: 배치 트랜잭션 처리
    - 📊 **리포트**: 안전재고 알림, 엑셀 내보내기

    ### 인증
    모든 API는 JWT Bearer 토큰 인증이 필요합니다.
    """,
    version="1.0.0",
    contact={
        "name": "DoneDone Team",
        "email": "dev@donedone.example.com"
    },
    license_info={
        "name": "MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "로컬 개발"},
        {"url": "https://api.donedone.example.com", "description": "프로덕션"},
    ]
)

# 태그 메타데이터
tags_metadata = [
    {
        "name": "제품 관리",
        "description": "제품 CRUD 및 바코드 조회",
    },
    {
        "name": "재고 관리",
        "description": "현재고 조회 및 입출고 처리",
    },
    {
        "name": "동기화",
        "description": "오프라인 트랜잭션 동기화",
    },
    {
        "name": "관리자",
        "description": "매장/카테고리 관리, 리포트 (ADMIN 전용)",
    },
]

app = FastAPI(openapi_tags=tags_metadata, ...)
```

### A-3. Postman/Insomnia Collection 생성 ✅

#### 체크리스트

- [x] OpenAPI 스펙에서 Collection 자동 생성
- [x] 환경 변수 설정 (dev, staging, prod)
- [x] 인증 토큰 자동 주입 설정
- [x] 예제 요청 데이터 포함

#### 구현 가이드

**1) OpenAPI JSON 내보내기 엔드포인트**

```python
# 이미 FastAPI가 제공: GET /openapi.json
# Postman에서 Import > Link > http://localhost:8000/openapi.json
```

**2) Postman 환경 변수 템플릿**

```json
// postman/environments/donedone-local.json
{
  "name": "DoneDone - Local",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "access_token",
      "value": "",
      "enabled": true
    }
  ]
}
```

**3) Collection Pre-request Script (인증 자동화)**

```javascript
// Postman Collection > Pre-request Script
if (!pm.environment.get("access_token")) {
  pm.sendRequest(
    {
      url: pm.environment.get("base_url") + "/auth/login",
      method: "POST",
      header: { "Content-Type": "application/json" },
      body: {
        mode: "raw",
        raw: JSON.stringify({
          email: pm.environment.get("test_email"),
          password: pm.environment.get("test_password"),
        }),
      },
    },
    function (err, res) {
      pm.environment.set("access_token", res.json().access_token);
    },
  );
}
```

### A-4. API 변경 이력 관리 ✅

#### 체크리스트

- [x] CHANGELOG.md 작성
- [x] Deprecated API 표시 방법 정의
- [x] 버전 관리 전략 수립 (URL vs Header)

#### 구현 가이드

```python
# Deprecated 엔드포인트 표시
@router.get(
    "/stocks",
    deprecated=True,
    summary="[Deprecated] 재고 조회 - /inventory/stocks 사용",
    description="이 엔드포인트는 v1.1에서 제거 예정입니다."
)
async def get_stocks_legacy():
    ...
```

---

## Phase B: 테스트 강화

**목표**: 코드 신뢰성 확보 및 리팩토링 안전망 구축  
**예상 기간**: 5-7일

### B-1. 테스트 커버리지 측정 및 목표 설정 ✅

#### 체크리스트

- [x] pytest-cov 설정
- [x] 커버리지 리포트 생성
- [x] 목표 커버리지 설정 (권장: 80% 이상)
- [x] CI에서 커버리지 체크 자동화

#### 구현 가이드

```bash
# 설치
pip install pytest-cov

# 실행
pytest --cov=app --cov-report=html --cov-report=term-missing

# pyproject.toml 설정
[tool.pytest.ini_options]
addopts = "--cov=app --cov-fail-under=80"

[tool.coverage.run]
source = ["app"]
omit = ["app/tests/*", "app/alembic/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

### B-2. 단위 테스트 보강 ✅

#### 체크리스트

- [x] 서비스 레이어 테스트 (비즈니스 로직)
- [x] 엣지 케이스 테스트 (경계값, null, 빈 값)
- [x] Mock 활용한 외부 의존성 격리

#### 구현 가이드

```python
# tests/unit/test_inventory_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.inventory import InventoryService
from app.exceptions import StockInsufficientError

class TestInventoryService:
    """재고 서비스 단위 테스트"""

    @pytest.fixture
    def mock_session(self):
        """Mock DB 세션"""
        session = AsyncMock()
        return session

    @pytest.fixture
    def service(self, mock_session):
        return InventoryService(mock_session)

    async def test_outbound_insufficient_stock_raises_error(
        self, service, mock_session
    ):
        """출고 시 재고 부족하면 예외 발생"""
        # Given
        mock_stock = MagicMock(quantity=5)
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_stock

        # When & Then
        with pytest.raises(StockInsufficientError) as exc_info:
            await service.process_outbound(
                product_id="...",
                store_id="...",
                quantity=10  # 재고(5)보다 많음
            )

        assert exc_info.value.available == 5
        assert exc_info.value.requested == 10

    async def test_outbound_success_updates_stock(self, service, mock_session):
        """정상 출고 시 재고 감소"""
        # Given
        mock_stock = MagicMock(quantity=10)
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_stock

        # When
        result = await service.process_outbound(
            product_id="...",
            store_id="...",
            quantity=3
        )

        # Then
        assert mock_stock.quantity == 7
        assert result.transaction_type == "OUTBOUND"

    @pytest.mark.parametrize("quantity,expected_status", [
        (0, "OUT_OF_STOCK"),
        (5, "LOW"),      # safe_stock=10 기준
        (10, "NORMAL"),
        (20, "GOOD"),
    ])
    async def test_calculate_stock_status(
        self, service, quantity, expected_status
    ):
        """재고량에 따른 상태 계산"""
        status = service.calculate_stock_status(
            quantity=quantity,
            safe_stock=10
        )
        assert status == expected_status
```

### B-3. 통합 테스트 보강 ✅

#### 체크리스트

- [x] 실제 DB를 사용한 API 테스트
- [x] 트랜잭션 롤백으로 테스트 격리
- [x] 테스트 데이터 Fixture 체계화

#### 구현 가이드

```python
# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db

# 테스트용 DB URL
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/donedone_test"

@pytest.fixture(scope="session")
def event_loop():
    """세션 스코프 이벤트 루프"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    """테스트 DB 엔진"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.fixture
async def db_session(test_engine):
    """각 테스트마다 트랜잭션 롤백"""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()

@pytest.fixture
async def client(db_session):
    """테스트 클라이언트"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

# 테스트 데이터 Fixtures
@pytest.fixture
async def sample_category(db_session):
    """샘플 카테고리"""
    from app.models import Category
    category = Category(name="스낵", description="과자류")
    db_session.add(category)
    await db_session.flush()
    return category

@pytest.fixture
async def sample_product(db_session, sample_category):
    """샘플 제품"""
    from app.models import Product
    product = Product(
        barcode="8801234567890",
        name="새우깡",
        category_id=sample_category.id,
        unit="봉",
        price=1500,
        safe_stock=10
    )
    db_session.add(product)
    await db_session.flush()
    return product
```

### B-4. 부하 테스트 (Performance Testing) ✅

#### 체크리스트

- [x] Locust 또는 k6 설정
- [x] 주요 시나리오 스크립트 작성
- [x] 성능 기준선(baseline) 측정
- [x] 병목 지점 식별

#### 구현 가이드

**Locust 설정**

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between
import random

class InventoryUser(HttpUser):
    """재고 관리 사용자 시뮬레이션"""
    wait_time = between(1, 3)

    def on_start(self):
        """로그인"""
        response = self.client.post("/auth/login", json={
            "email": "worker@test.com",
            "password": "testpass123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(10)
    def scan_barcode(self):
        """바코드 스캔 (가장 빈번한 작업)"""
        barcodes = ["8801234567890", "8801234567891", "8801234567892"]
        barcode = random.choice(barcodes)
        self.client.get(
            f"/products/barcode/{barcode}",
            headers=self.headers,
            name="/products/barcode/[barcode]"
        )

    @task(5)
    def check_stock(self):
        """재고 확인"""
        self.client.get(
            "/inventory/stocks",
            headers=self.headers,
            params={"store_id": "my-store-id"}
        )

    @task(3)
    def process_inbound(self):
        """입고 처리"""
        self.client.post(
            "/inventory/inbound",
            headers=self.headers,
            json={
                "product_id": "sample-product-id",
                "store_id": "my-store-id",
                "quantity": random.randint(1, 10),
                "note": "테스트 입고"
            }
        )

    @task(2)
    def process_outbound(self):
        """출고 처리"""
        self.client.post(
            "/inventory/outbound",
            headers=self.headers,
            json={
                "product_id": "sample-product-id",
                "store_id": "my-store-id",
                "quantity": random.randint(1, 3)
            }
        )

    @task(1)
    def sync_offline_transactions(self):
        """오프라인 동기화 (배치)"""
        transactions = [
            {
                "local_id": f"local-{i}",
                "type": "INBOUND",
                "product_id": "sample-product-id",
                "quantity": 5
            }
            for i in range(10)
        ]
        self.client.post(
            "/sync/transactions",
            headers=self.headers,
            json={"transactions": transactions}
        )
```

**실행 방법**

```bash
# 설치
pip install locust

# 실행 (Web UI)
locust -f tests/load/locustfile.py --host=http://localhost:8000

# 실행 (Headless)
locust -f tests/load/locustfile.py \
    --host=http://localhost:8000 \
    --users 100 \
    --spawn-rate 10 \
    --run-time 5m \
    --headless \
    --csv=results/load_test
```

**k6 대안 (더 가벼움)**

```javascript
// tests/load/k6-script.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 20 }, // Ramp up
    { duration: "1m", target: 50 }, // Stay
    { duration: "30s", target: 0 }, // Ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<200"], // 95%가 200ms 이내
    http_req_failed: ["rate<0.01"], // 에러율 1% 미만
  },
};

export default function () {
  const BASE_URL = "http://localhost:8000";

  // 바코드 조회
  const res = http.get(`${BASE_URL}/products/barcode/8801234567890`);

  check(res, {
    "status is 200": (r) => r.status === 200,
    "response time < 100ms": (r) => r.timings.duration < 100,
  });

  sleep(1);
}
```

### B-5. 계약 테스트 (Contract Testing) ✅

#### 체크리스트

- [x] Pact 또는 Schemathesis 설정
- [x] 프론트엔드-백엔드 스키마 일치 검증
- [x] CI에서 자동 검증

#### 구현 가이드

```python
# tests/contract/test_openapi_contract.py
import schemathesis
from hypothesis import settings, Phase

schema = schemathesis.from_uri("http://localhost:8000/openapi.json")

@schema.parametrize()
@settings(max_examples=50, phases=[Phase.explicit, Phase.generate])
def test_api_contract(case):
    """OpenAPI 스펙 기반 자동 계약 테스트"""
    response = case.call()
    case.validate_response(response)
```

---

## Phase C: 에러 핸들링 & 로깅 체계

**목표**: 운영 환경에서 문제 발생 시 빠른 디버깅이 가능하도록 함  
**예상 기간**: 3-4일

### C-1. 커스텀 예외 계층 구축 ✅

#### 체크리스트

- [x] 베이스 예외 클래스 정의
- [x] 도메인별 예외 클래스 정의
- [x] 글로벌 예외 핸들러 등록
- [x] 에러 코드 체계 수립

#### 구현 가이드

```python
# app/exceptions/__init__.py
from typing import Any, Optional

class DoneDoneException(Exception):
    """베이스 예외 클래스"""
    error_code: str = "INTERNAL_ERROR"
    status_code: int = 500
    message: str = "서버 내부 오류가 발생했습니다"

    def __init__(
        self,
        message: Optional[str] = None,
        detail: Optional[Any] = None
    ):
        self.message = message or self.__class__.message
        self.detail = detail
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "detail": self.detail
        }


# 인증 관련
class AuthenticationError(DoneDoneException):
    error_code = "AUTHENTICATION_FAILED"
    status_code = 401
    message = "인증에 실패했습니다"

class AuthorizationError(DoneDoneException):
    error_code = "FORBIDDEN"
    status_code = 403
    message = "접근 권한이 없습니다"


# 제품 관련
class ProductNotFoundError(DoneDoneException):
    error_code = "PRODUCT_NOT_FOUND"
    status_code = 404
    message = "제품을 찾을 수 없습니다"

class DuplicateBarcodeError(DoneDoneException):
    error_code = "DUPLICATE_BARCODE"
    status_code = 409
    message = "이미 등록된 바코드입니다"


# 재고 관련
class StockInsufficientError(DoneDoneException):
    error_code = "STOCK_INSUFFICIENT"
    status_code = 400
    message = "재고가 부족합니다"

    def __init__(self, available: int, requested: int):
        self.available = available
        self.requested = requested
        super().__init__(
            message=f"재고 부족: 가용 {available}개, 요청 {requested}개",
            detail={"available": available, "requested": requested}
        )

class StockNotFoundError(DoneDoneException):
    error_code = "STOCK_NOT_FOUND"
    status_code = 404
    message = "해당 매장에 재고 정보가 없습니다"


# 동기화 관련
class SyncConflictError(DoneDoneException):
    error_code = "SYNC_CONFLICT"
    status_code = 409
    message = "동기화 충돌이 발생했습니다"

class DuplicateLocalIdError(DoneDoneException):
    error_code = "DUPLICATE_LOCAL_ID"
    status_code = 409
    message = "이미 처리된 트랜잭션입니다"
```

**글로벌 예외 핸들러**

```python
# app/exceptions/handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

from app.exceptions import DoneDoneException

logger = logging.getLogger(__name__)

async def donedone_exception_handler(
    request: Request,
    exc: DoneDoneException
) -> JSONResponse:
    """커스텀 예외 핸들러"""
    logger.warning(
        f"Business error: {exc.error_code}",
        extra={
            "error_code": exc.error_code,
            "path": request.url.path,
            "detail": exc.detail
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

async def integrity_error_handler(
    request: Request,
    exc: IntegrityError
) -> JSONResponse:
    """DB 무결성 오류 핸들러"""
    logger.error(f"Database integrity error: {exc}")
    return JSONResponse(
        status_code=409,
        content={
            "error_code": "DATA_CONFLICT",
            "message": "데이터 충돌이 발생했습니다",
            "detail": str(exc.orig) if exc.orig else None
        }
    )

async def unhandled_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """예상치 못한 예외 핸들러"""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "message": "서버 내부 오류가 발생했습니다"
        }
    )

# main.py에 등록
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from app.exceptions import DoneDoneException
from app.exceptions.handlers import (
    donedone_exception_handler,
    integrity_error_handler,
    unhandled_exception_handler
)

app = FastAPI()
app.add_exception_handler(DoneDoneException, donedone_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
```

### C-2. 구조화된 로깅 (Structured Logging) ✅

#### 체크리스트

- [x] structlog 또는 python-json-logger 설정
- [x] 로그 레벨 정책 수립
- [x] Request/Response 로깅 미들웨어
- [x] 민감 정보 마스킹

#### 구현 가이드

```python
# app/core/logging.py
import logging
import sys
from typing import Any
import structlog
from structlog.types import EventDict

def setup_logging(json_logs: bool = False, log_level: str = "INFO"):
    """로깅 설정"""

    # 민감 정보 마스킹 프로세서
    def mask_sensitive_data(
        logger: logging.Logger,
        method_name: str,
        event_dict: EventDict
    ) -> EventDict:
        sensitive_keys = {"password", "token", "secret", "authorization"}

        for key in list(event_dict.keys()):
            if any(s in key.lower() for s in sensitive_keys):
                event_dict[key] = "***MASKED***"

        return event_dict

    # 공통 프로세서
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        mask_sensitive_data,
    ]

    if json_logs:
        # 프로덕션: JSON 로그
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        # 개발: 컬러 콘솔 로그
        shared_processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # 표준 라이브러리 로거 설정
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level),
    )

# 사용 예시
import structlog
logger = structlog.get_logger()

async def process_outbound(product_id: str, quantity: int):
    logger.info(
        "Processing outbound",
        product_id=product_id,
        quantity=quantity
    )
    # ...
    logger.info(
        "Outbound completed",
        product_id=product_id,
        remaining_stock=remaining
    )
```

### C-3. Request ID 추적 (Correlation ID) ✅

#### 체크리스트

- [x] Request ID 미들웨어 구현
- [x] 모든 로그에 Request ID 포함
- [x] 응답 헤더에 Request ID 포함

#### 구현 가이드

```python
# app/middleware/request_id.py
import uuid
from contextvars import ContextVar
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

# Context variable for request ID
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 헤더에서 ID 가져오거나 새로 생성
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_ctx.set(request_id)

        # structlog context에 바인딩
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response

# main.py
app.add_middleware(RequestIdMiddleware)
```

### C-4. Request/Response 로깅 ✅

#### 체크리스트

- [x] 요청 정보 로깅 (path, method, params)
- [x] 응답 정보 로깅 (status, duration)
- [x] 대용량 body 로깅 제한
- [x] 헬스체크 등 노이즈 필터링

#### 구현 가이드

```python
# app/middleware/logging.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    # 로깅 제외 경로
    EXCLUDE_PATHS = {"/health", "/ready", "/metrics", "/docs", "/openapi.json"}

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.EXCLUDE_PATHS:
            return await call_next(request)

        start_time = time.perf_counter()

        # 요청 로깅
        logger.info(
            "Request started",
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
        )

        response = await call_next(request)

        # 응답 로깅
        duration_ms = (time.perf_counter() - start_time) * 1000

        log_method = logger.info if response.status_code < 400 else logger.warning
        log_method(
            "Request completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2)
        )

        return response
```

---

## Phase D: 쿼리 최적화 & 벤치마크

**목표**: 주요 API의 응답 시간을 측정하고 최적화  
**예상 기간**: 4-5일

### D-1. 쿼리 분석 환경 구축

#### 체크리스트

- [ ] SQLAlchemy echo 모드 설정
- [ ] PostgreSQL slow query log 활성화
- [ ] EXPLAIN ANALYZE 활용법 숙지

#### 구현 가이드

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine
import logging

# 개발 환경에서 쿼리 로깅
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # SQL 출력
    echo_pool=settings.DEBUG,  # 커넥션 풀 이벤트 출력
)

# 또는 특정 쿼리만 분석
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
```

```sql
-- PostgreSQL 슬로우 쿼리 설정 (postgresql.conf)
log_min_duration_statement = 100  -- 100ms 이상 쿼리 로깅
log_statement = 'none'  -- 모든 쿼리 로깅 비활성화 (슬로우만)
```

### D-2. N+1 문제 점검 및 해결

#### 체크리스트

- [ ] 현재 코드에서 N+1 발생 지점 식별
- [ ] `selectinload`, `joinedload` 적용
- [ ] 적용 전/후 쿼리 수 비교

#### 구현 가이드

```python
# Before: N+1 문제 발생
async def get_stocks_bad(store_id: UUID) -> list[CurrentStock]:
    result = await session.execute(
        select(CurrentStock).where(CurrentStock.store_id == store_id)
    )
    stocks = result.scalars().all()

    # 각 stock마다 product를 개별 조회 (N+1)
    for stock in stocks:
        _ = stock.product.name  # Lazy loading 발생!

    return stocks

# After: Eager Loading으로 해결
from sqlalchemy.orm import selectinload, joinedload

async def get_stocks_good(store_id: UUID) -> list[CurrentStock]:
    result = await session.execute(
        select(CurrentStock)
        .where(CurrentStock.store_id == store_id)
        .options(
            # 1:N 관계 - selectinload (별도 IN 쿼리)
            selectinload(CurrentStock.product)
            .selectinload(Product.category),
            # N:1 관계 - joinedload (JOIN으로 한 번에)
            joinedload(CurrentStock.store)
        )
    )
    return result.scalars().unique().all()
```

**언제 어떤 로딩 전략을 사용할지:**

| 전략              | 용도                   | 예시                 |
| ----------------- | ---------------------- | -------------------- |
| `selectinload`    | 1:N, N:M 관계          | Stock → Transactions |
| `joinedload`      | N:1, 1:1 관계          | Stock → Product      |
| `subqueryload`    | 복잡한 1:N (집계 필요) | -                    |
| `lazyload` (기본) | 필요할 때만 로드       | 드물게 접근하는 관계 |

### D-3. 인덱스 최적화

#### 체크리스트

- [ ] 주요 쿼리의 EXPLAIN ANALYZE 실행
- [ ] 필요한 인덱스 추가
- [ ] 불필요한 인덱스 제거
- [ ] 복합 인덱스 설계

#### 구현 가이드

```sql
-- 현재 인덱스 확인
SELECT
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    tablename = 'current_stocks';

-- 쿼리 실행계획 분석
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT cs.*, p.name, p.barcode
FROM current_stocks cs
JOIN products p ON cs.product_id = p.id
WHERE cs.store_id = 'xxx'
  AND cs.quantity < p.safe_stock;

-- 결과 해석:
-- Seq Scan: 전체 테이블 스캔 (비효율)
-- Index Scan: 인덱스 사용 (효율)
-- Bitmap Index Scan: 여러 인덱스 결합

-- 필요한 인덱스 추가
CREATE INDEX CONCURRENTLY idx_current_stocks_store_product
ON current_stocks(store_id, product_id);

CREATE INDEX CONCURRENTLY idx_transactions_created_at
ON inventory_transactions(created_at DESC);

-- 부분 인덱스 (조건부)
CREATE INDEX CONCURRENTLY idx_stocks_low_quantity
ON current_stocks(store_id, product_id)
WHERE quantity < 10;  -- 안전재고 미만만 인덱싱
```

**Alembic 마이그레이션으로 인덱스 추가:**

```python
# alembic/versions/xxxx_add_indexes.py
def upgrade():
    op.create_index(
        'idx_current_stocks_store_product',
        'current_stocks',
        ['store_id', 'product_id'],
        unique=False
    )
    op.create_index(
        'idx_transactions_created_at',
        'inventory_transactions',
        [sa.text('created_at DESC')],
        unique=False
    )

def downgrade():
    op.drop_index('idx_current_stocks_store_product')
    op.drop_index('idx_transactions_created_at')
```

### D-4. Connection Pool 튜닝

#### 체크리스트

- [ ] 현재 pool 설정 확인
- [ ] 동시 접속 수 기반 적정값 계산
- [ ] pool_pre_ping 활성화 (연결 상태 확인)

#### 구현 가이드

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

def create_engine(settings):
    """환경별 엔진 설정"""

    if settings.TESTING:
        # 테스트: 풀 없음
        return create_async_engine(
            settings.DATABASE_URL,
            poolclass=NullPool
        )

    # 프로덕션: 풀 설정
    return create_async_engine(
        settings.DATABASE_URL,
        pool_size=10,           # 기본 연결 수
        max_overflow=20,        # 추가 허용 연결 수
        pool_timeout=30,        # 연결 대기 타임아웃
        pool_recycle=1800,      # 30분마다 연결 재생성
        pool_pre_ping=True,     # 사용 전 연결 상태 확인
        echo_pool=settings.DEBUG
    )
```

**적정 pool_size 계산:**

```
pool_size = (코어 수 * 2) + 1  (일반적 권장)

예: 4코어 서버
pool_size = (4 * 2) + 1 = 9 ~ 10
max_overflow = pool_size * 2 = 20
```

### D-5. 벤치마크 및 성능 기준선

#### 체크리스트

- [ ] 주요 API 응답 시간 측정
- [ ] 성능 목표 설정
- [ ] 벤치마크 자동화

#### 구현 가이드

```python
# tests/benchmark/test_api_performance.py
import pytest
import time
from statistics import mean, stdev

class TestAPIPerformance:
    """API 성능 벤치마크"""

    ITERATIONS = 100

    @pytest.fixture
    def performance_results(self):
        return {}

    async def measure(self, client, method, url, **kwargs):
        """응답 시간 측정"""
        times = []
        for _ in range(self.ITERATIONS):
            start = time.perf_counter()
            response = await getattr(client, method)(url, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            assert response.status_code < 400

        return {
            "min": min(times),
            "max": max(times),
            "mean": mean(times),
            "stdev": stdev(times),
            "p50": sorted(times)[len(times) // 2],
            "p95": sorted(times)[int(len(times) * 0.95)],
            "p99": sorted(times)[int(len(times) * 0.99)],
        }

    async def test_barcode_lookup_performance(self, client):
        """바코드 조회 < 100ms (P95)"""
        stats = await self.measure(
            client, "get", "/products/barcode/8801234567890"
        )
        print(f"\n바코드 조회: {stats}")
        assert stats["p95"] < 100, f"P95 {stats['p95']}ms > 100ms"

    async def test_stock_list_performance(self, client):
        """재고 목록 < 200ms (P95)"""
        stats = await self.measure(
            client, "get", "/inventory/stocks",
            params={"store_id": "xxx"}
        )
        print(f"\n재고 목록: {stats}")
        assert stats["p95"] < 200, f"P95 {stats['p95']}ms > 200ms"

    async def test_inbound_performance(self, client):
        """입고 처리 < 300ms (P95)"""
        stats = await self.measure(
            client, "post", "/inventory/inbound",
            json={"product_id": "xxx", "store_id": "xxx", "quantity": 1}
        )
        print(f"\n입고 처리: {stats}")
        assert stats["p95"] < 300, f"P95 {stats['p95']}ms > 300ms"
```

**성능 목표 (SLO):**

| API           | P95 목표 | P99 목표 |
| ------------- | -------- | -------- |
| 바코드 조회   | < 100ms  | < 200ms  |
| 재고 목록     | < 200ms  | < 500ms  |
| 입고/출고     | < 300ms  | < 500ms  |
| 동기화 (10건) | < 1000ms | < 2000ms |

---

## Phase E: 인프라 & 배포

**목표**: 일관된 개발/배포 환경 구축  
**예상 기간**: 3-4일

### E-1. Docker 개발 환경

#### 체크리스트

- [ ] Dockerfile 작성 (멀티 스테이지 빌드)
- [ ] docker-compose.yml 작성
- [ ] .dockerignore 설정
- [ ] 로컬 개발 원클릭 실행

#### 구현 가이드

```dockerfile
# Dockerfile
# === Build Stage ===
FROM python:3.12-slim as builder

WORKDIR /app

# Poetry 설치
RUN pip install poetry==1.7.1

# 의존성 먼저 복사 (캐시 활용)
COPY pyproject.toml poetry.lock ./

# 가상환경 생성 및 의존성 설치
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-dev --no-root

# === Production Stage ===
FROM python:3.12-slim as production

WORKDIR /app

# 비root 사용자 생성
RUN useradd --create-home appuser
USER appuser

# 가상환경 복사
COPY --from=builder /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# 애플리케이션 코드 복사
COPY --chown=appuser:appuser ./app ./app
COPY --chown=appuser:appuser ./alembic ./alembic
COPY --chown=appuser:appuser alembic.ini .

# 헬스체크
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/donedone
      - ENVIRONMENT=development
      - DEBUG=true
    depends_on:
      db:
        condition: service_healthy
    volumes:
      # 개발 시 코드 변경 반영
      - ./app:/app/app:ro
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=donedone
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  # 선택: Redis (캐싱, Rate Limiting용)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

volumes:
  postgres_data:
```

```yaml
# docker-compose.dev.yml (개발용 오버라이드)
version: "3.8"

services:
  api:
    build:
      target: builder # 개발 의존성 포함
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    environment:
      - DEBUG=true
```

**실행 방법:**

```bash
# 개발 환경 실행
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# 프로덕션 모드
docker-compose up -d

# 로그 확인
docker-compose logs -f api

# DB 마이그레이션
docker-compose exec api alembic upgrade head
```

### E-2. Health Check 엔드포인트

#### 체크리스트

- [ ] `/health` - 기본 헬스체크
- [ ] `/ready` - 의존성 상태 확인 (DB 연결 등)
- [ ] 메트릭 엔드포인트 (선택)

#### 구현 가이드

```python
# app/api/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api.deps import get_db

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    기본 헬스체크

    컨테이너가 실행 중인지만 확인
    """
    return {"status": "healthy"}

@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    준비 상태 확인

    DB 연결 등 의존성 상태 확인
    """
    checks = {}

    # DB 연결 확인
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Redis 연결 확인 (사용 시)
    # try:
    #     await redis.ping()
    #     checks["redis"] = "healthy"
    # except Exception as e:
    #     checks["redis"] = f"unhealthy: {str(e)}"

    all_healthy = all(v == "healthy" for v in checks.values())

    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks
    }

# main.py
app.include_router(health_router)
```

### E-3. 환경 설정 관리

#### 체크리스트

- [ ] pydantic-settings로 환경변수 검증
- [ ] 환경별 설정 분리
- [ ] 비밀값 관리 전략

#### 구현 가이드

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """애플리케이션 설정"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # 환경
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # 데이터베이스
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # 인증
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # 로깅
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False  # 프로덕션에서 True

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str) -> str:
        if v.startswith("postgres://"):
            # asyncpg 호환 URL로 변환
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

@lru_cache
def get_settings() -> Settings:
    """싱글톤 설정 객체"""
    return Settings()

settings = get_settings()
```

```bash
# .env.example
ENVIRONMENT=development
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/donedone
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60

CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

LOG_LEVEL=DEBUG
LOG_JSON=false
```

### E-4. CI/CD 파이프라인

#### 체크리스트

- [ ] GitHub Actions 워크플로우
- [ ] 테스트 자동화
- [ ] 린트/타입 체크
- [ ] Docker 이미지 빌드 (선택)

#### 구현 가이드

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12"

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install ruff mypy

      - name: Run Ruff (lint)
        run: ruff check .

      - name: Run Ruff (format check)
        run: ruff format --check .

      - name: Run MyPy
        run: mypy app --ignore-missing-imports

  test:
    runs-on: ubuntu-latest
    needs: lint

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: donedone_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install Poetry
        run: pip install poetry

      - name: Install dependencies
        run: poetry install

      - name: Run migrations
        run: poetry run alembic upgrade head
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/donedone_test

      - name: Run tests with coverage
        run: |
          poetry run pytest \
            --cov=app \
            --cov-report=xml \
            --cov-fail-under=80
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/donedone_test
          SECRET_KEY: test-secret-key

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t donedone-api:${{ github.sha }} .

      # 선택: Docker Hub 또는 GitHub Container Registry 푸시
      # - name: Push to registry
      #   run: ...
```

---

## Phase F: 보안 강화

**목표**: 프로덕션 환경에서의 보안 위협 방어  
**예상 기간**: 3-4일

### F-1. Rate Limiting

#### 체크리스트

- [ ] slowapi 설정
- [ ] 엔드포인트별 제한 설정
- [ ] Rate limit 초과 시 응답 커스터마이징

#### 구현 가이드

```python
# app/core/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

async def rate_limit_exceeded_handler(
    request: Request,
    exc: RateLimitExceeded
) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error_code": "RATE_LIMIT_EXCEEDED",
            "message": "요청 횟수가 제한을 초과했습니다",
            "detail": {
                "limit": exc.detail,
                "retry_after": request.state.view_rate_limit
            }
        }
    )

# main.py
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# 라우터에서 사용
from app.core.rate_limit import limiter

@router.post("/auth/login")
@limiter.limit("5/minute")  # 분당 5회
async def login(request: Request, ...):
    ...

@router.get("/products/barcode/{barcode}")
@limiter.limit("100/minute")  # 분당 100회
async def get_product(request: Request, ...):
    ...

@router.post("/sync/transactions")
@limiter.limit("10/minute")  # 배치 동기화는 더 제한적
async def sync_transactions(request: Request, ...):
    ...
```

### F-2. Input Validation 강화

#### 체크리스트

- [ ] 문자열 길이 제한
- [ ] 패턴 검증 (바코드, 이메일 등)
- [ ] 숫자 범위 검증
- [ ] Strict mode 활성화

#### 구현 가이드

```python
# app/schemas/products.py
from pydantic import BaseModel, Field, field_validator
import re

class ProductCreate(BaseModel):
    """제품 생성 스키마"""

    model_config = {"strict": True}  # 타입 강제

    barcode: str = Field(
        ...,
        min_length=8,
        max_length=14,
        description="EAN-8/13/14 바코드"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="제품명"
    )
    price: int = Field(
        ...,
        ge=0,
        le=100_000_000,  # 1억 이하
        description="가격 (원)"
    )
    safe_stock: int = Field(
        default=10,
        ge=0,
        le=100_000,
        description="안전재고"
    )

    @field_validator("barcode")
    @classmethod
    def validate_barcode(cls, v: str) -> str:
        # 숫자만 허용
        if not v.isdigit():
            raise ValueError("바코드는 숫자만 포함해야 합니다")
        # 체크섬 검증 (EAN-13)
        if len(v) == 13 and not cls._validate_ean13_checksum(v):
            raise ValueError("유효하지 않은 EAN-13 바코드입니다")
        return v

    @staticmethod
    def _validate_ean13_checksum(barcode: str) -> bool:
        """EAN-13 체크섬 검증"""
        total = sum(
            int(d) * (1 if i % 2 == 0 else 3)
            for i, d in enumerate(barcode[:12])
        )
        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(barcode[12])

class TransactionCreate(BaseModel):
    """트랜잭션 생성 스키마"""

    quantity: int = Field(
        ...,
        gt=0,  # 0보다 커야 함
        le=10_000,  # 최대 10,000개
        description="수량"
    )
    note: str | None = Field(
        default=None,
        max_length=500,
        description="메모"
    )

    @field_validator("note")
    @classmethod
    def sanitize_note(cls, v: str | None) -> str | None:
        if v is None:
            return None
        # 위험 문자 제거
        v = v.strip()
        # HTML 태그 제거
        v = re.sub(r'<[^>]+>', '', v)
        return v
```

### F-3. CORS 설정 검토

#### 체크리스트

- [ ] 허용 Origin 목록 관리
- [ ] 환경별 설정 분리
- [ ] Credentials 설정 검토

#### 구현 가이드

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI, settings: Settings):
    """CORS 설정"""

    if settings.is_production:
        # 프로덕션: 명시적 Origin만 허용
        origins = settings.CORS_ORIGINS
    else:
        # 개발: 로컬 개발 서버 허용
        origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
        max_age=600,  # Preflight 캐시 10분
    )
```

### F-4. SQL Injection 방어 점검

#### 체크리스트

- [ ] Raw SQL 사용처 점검
- [ ] 파라미터 바인딩 확인
- [ ] 동적 쿼리 안전성 검토

#### 구현 가이드

```python
# ❌ 위험: 문자열 포맷팅
async def search_products_bad(query: str):
    result = await session.execute(
        text(f"SELECT * FROM products WHERE name LIKE '%{query}%'")
    )
    return result.fetchall()

# ✅ 안전: 파라미터 바인딩
async def search_products_good(query: str):
    result = await session.execute(
        text("SELECT * FROM products WHERE name LIKE :query"),
        {"query": f"%{query}%"}
    )
    return result.fetchall()

# ✅ 더 안전: ORM 사용
async def search_products_best(query: str):
    result = await session.execute(
        select(Product).where(Product.name.ilike(f"%{query}%"))
    )
    return result.scalars().all()
```

### F-5. 보안 헤더 설정

#### 체크리스트

- [ ] Security headers 미들웨어 추가
- [ ] HTTPS 강제 (프로덕션)
- [ ] Content-Type 검증

#### 구현 가이드

```python
# app/middleware/security.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """보안 헤더 추가"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # XSS 방어
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer 정책
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy (API용 간소화)
        response.headers["Content-Security-Policy"] = "default-src 'none'"

        return response

# main.py
app.add_middleware(SecurityHeadersMiddleware)

# HTTPS 강제 (프로덕션)
if settings.is_production:
    from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
    app.add_middleware(HTTPSRedirectMiddleware)
```

---

## 📅 예상 일정 (파트타임 기준)

| 주차  | Phase                               | 예상 소요 |
| ----- | ----------------------------------- | --------- |
| 1주차 | A. API 문서화                       | 3-4일     |
| 2주차 | B. 테스트 강화 (1/2)                | 3-4일     |
| 3주차 | B. 테스트 강화 (2/2) + C. 에러/로깅 | 4-5일     |
| 4주차 | D. 쿼리 최적화                      | 4-5일     |
| 5주차 | E. 인프라/배포                      | 3-4일     |
| 6주차 | F. 보안 강화                        | 3-4일     |

---

## 🎯 완료 기준

### Phase A 완료 기준 ✅

- [x] 프론트엔드 개발자가 Swagger만 보고 API 연동 가능
- [x] Postman Collection으로 모든 API 테스트 가능
- [x] 에러 응답에 명확한 error_code와 메시지 포함

### Phase B 완료 기준

- [ ] 테스트 커버리지 80% 이상
- [ ] 부하 테스트로 P95 응답 시간 측정 완료
- [ ] CI에서 모든 테스트 자동 실행

### Phase C 완료 기준

- [ ] 모든 에러에 request_id 추적 가능
- [ ] JSON 로그로 Kibana/Loki 연동 가능
- [ ] 민감 정보 로그에 노출 안 됨

### Phase D 완료 기준

- [ ] 바코드 조회 P95 < 100ms
- [ ] N+1 쿼리 0건
- [ ] 주요 쿼리 모두 인덱스 활용

### Phase E 완료 기준

- [ ] `docker-compose up`으로 로컬 환경 원클릭 실행
- [ ] GitHub PR마다 자동 테스트 실행
- [ ] Health check로 서비스 상태 확인 가능

### Phase F 완료 기준

- [ ] Rate limiting 동작 확인
- [ ] 모든 입력값 검증 통과
- [ ] 보안 헤더 적용 확인

---

**작성자**: Claude  
**버전**: 1.0.0  
**최종 업데이트**: 2026-01-24
