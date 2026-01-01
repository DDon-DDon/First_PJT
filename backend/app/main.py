from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="똔똔(DoneDone) 오프라인 매장 재고 관리 시스템 API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check 엔드포인트
@app.get("/health", tags=["Health"])
async def health_check():
    """
    서버 상태 확인

    Returns:
        dict: 서버 상태 정보
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root 엔드포인트
@app.get("/", tags=["Root"])
async def root():
    """
    API 루트 엔드포인트

    Returns:
        dict: API 정보
    """
    return {
        "message": "Welcome to DoneDone API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# TODO: API 라우터 등록
# from app.api.v1 import auth, products, inventory, transactions, sync
# app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Auth"])
# app.include_router(products.router, prefix=f"{settings.API_V1_PREFIX}/products", tags=["Products"])
# app.include_router(inventory.router, prefix=f"{settings.API_V1_PREFIX}/inventory", tags=["Inventory"])
# app.include_router(transactions.router, prefix=f"{settings.API_V1_PREFIX}/transactions", tags=["Transactions"])
# app.include_router(sync.router, prefix=f"{settings.API_V1_PREFIX}/sync", tags=["Sync"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
