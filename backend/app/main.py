"""
FastAPI 애플리케이션 엔트리포인트 (Application Entry Point)

파일 역할:
    FastAPI 애플리케이션을 생성하고 설정하는 메인 파일입니다.
    CORS, 미들웨어, 라우터 등을 설정하고 앱을 실행합니다.

패턴:
    - Application Factory 패턴: FastAPI 인스턴스 생성 및 설정
    - Middleware 패턴: 요청/응답 처리 전후에 공통 로직 실행
    - Router 패턴: 엔드포인트를 모듈별로 분리하여 등록

작성일: 2025-12-31
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import ApiException

# ========== API 문서 설정 ==========

description = """
# 똔똔(DoneDone) API 문서

오프라인 매장 재고 관리 시스템 **똔똔**의 백엔드 API입니다.

## 🔐 인증 (Authentication)

대부분의 API는 **Bearer Token** 인증이 필요합니다.
로그인 후 발급받은 `accessToken`을 HTTP 헤더에 포함하여 요청해주세요.

`Authorization: Bearer <your_access_token>`

## 🚀 주요 기능

* **제품(Products)**: 바코드 기반 제품 조회 및 관리
* **재고(Inventory)**: 매장별 실시간 재고 현황 및 상태(안전재고) 확인
* **트랜잭션(Transactions)**: 입고, 출고, 조정 이력 관리
* **동기화(Sync)**: 오프라인 작업 내역 일괄 동기화

## ⚠️ 공통 에러 응답 형식

모든 에러 응답은 아래와 같은 일관된 형식을 가집니다.

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "상세 에러 메시지",
    "details": {}
  }
}
```
"""

tags_metadata = [
    {"name": "Products", "description": "제품 마스터 데이터 조회 및 등록"},
    {"name": "Inventory", "description": "매장별 현재고 조회 및 상태 확인"},
    {"name": "Transactions", "description": "재고 입/출고 및 조정 트랜잭션 처리"},
    {"name": "Sync", "description": "오프라인 데이터 일괄 동기화"},
    {"name": "Stores", "description": "매장 기초 정보"},
    {"name": "Categories", "description": "카테고리 기초 정보"},
    {"name": "Admin", "description": "관리자 리포트 및 엑셀 추출"},
    {"name": "Health", "description": "서버 상태 확인"},
]

# ========== FastAPI 앱 인스턴스 생성 ==========

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=description,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "DoneDone Team",
        "email": "dev@donedone.example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "로컬 개발 서버"},
        {"url": "https://api.donedone.example.com", "description": "프로덕션 서버"},
    ]
)


# ========== CORS 미들웨어 설정 ==========

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 예외 핸들러 등록 ==========

@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    """
    커스텀 API 예외 처리
    정의된 에러 코드와 메시지를 JSON 형식으로 반환합니다.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Pydantic 검증 에러 처리 (422)
    FastAPI 기본 에러 형식을 프로젝트 표준 형식으로 변환합니다.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "입력값이 올바르지 않습니다.",
                "details": {"errors": exc.errors()},
            },
        },
    )


@app.exception_handler(Exception)
async def uncaught_exception_handler(request: Request, exc: Exception):
    """
    처리되지 않은 예외 처리 (500)
    내부 서버 에러를 반환하고, 실제 에러 내용은 (로깅이 추가되면) 로그에 남깁니다.
    """
    # TODO: 로깅 추가 (Phase C-2)
    # logger.error(f"Uncaught error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다.",
                "details": None,  # 보안상 상세 내용은 숨김
            },
        },
    )


# ========== 기본 엔드포인트 ==========

@app.get("/health", tags=["Health"])
async def health_check():
    """서버 상태 확인 (Health Check)"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/", tags=["Root"])
async def root():
    """API 루트 엔드포인트 (Welcome)"""
    return {
        "message": "Welcome to DoneDone API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# ========== API 라우터 등록 ==========

from app.api.v1 import products, inventory, transactions, sync, stores, categories, admin

app.include_router(
    products.router,
    prefix=f"{settings.API_V1_PREFIX}/products",
    tags=["Products"]
)

app.include_router(
    inventory.router,
    prefix=f"{settings.API_V1_PREFIX}/inventory",
    tags=["Inventory"]
)

app.include_router(
    transactions.router,
    prefix=f"{settings.API_V1_PREFIX}/transactions",
    tags=["Transactions"]
)

app.include_router(
    sync.router,
    prefix=f"{settings.API_V1_PREFIX}/sync",
    tags=["Sync"]
)

app.include_router(
    stores.router,
    prefix=f"{settings.API_V1_PREFIX}/stores",
    tags=["Stores"]
)

app.include_router(
    categories.router,
    prefix=f"{settings.API_V1_PREFIX}/categories",
    tags=["Categories"]
)

app.include_router(
    admin.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Admin"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )