"""
FastAPI 애플리케이션 엔트리포인트 (Application Entry Point)

파일 역할:
    FastAPI 애플리케이션을 생성하고 설정하는 메인 파일입니다.
    CORS, 미들웨어, 라우터 등을 설정하고 앱을 실행합니다.

패턴:
    - Application Factory 패턴: FastAPI 인스턴스 생성 및 설정
    - Middleware 패턴: 요청/응답 처리 전후에 공통 로직 실행
    - Router 패턴: 엔드포인트를 모듈별로 분리하여 등록

사용 목적:
    1. FastAPI 애플리케이션 인스턴스 생성
    2. CORS 설정 (프론트엔드 접근 허용)
    3. API 라우터 등록 (추후 구현)
    4. 기본 헬스체크 엔드포인트 제공

작성일: 2025-12-31
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


# ========== FastAPI 앱 인스턴스 생성 ==========

# FastAPI 애플리케이션
# 목적:
#   웹 API 서버의 핵심 객체입니다.
#   모든 엔드포인트, 미들웨어, 설정을 관리합니다.
#
# 주요 설정:
#   - title: API 문서 제목 (Swagger UI, ReDoc)
#   - version: API 버전
#   - description: API 설명
#   - docs_url: Swagger UI 경로 (/docs)
#   - redoc_url: ReDoc 경로 (/redoc)
#   - openapi_url: OpenAPI 스키마 경로 (/openapi.json)
#
# 자동 문서화:
#   FastAPI는 자동으로 API 문서를 생성합니다.
#   - Swagger UI: http://localhost:8000/docs
#   - ReDoc: http://localhost:8000/redoc
#   - OpenAPI 스펙: http://localhost:8000/openapi.json
app = FastAPI(
    title=settings.PROJECT_NAME,  # "DoneDone API"
    version=settings.VERSION,  # "1.0.0"
    description="똔똔(DoneDone) 오프라인 매장 재고 관리 시스템 API",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json"  # OpenAPI 스펙 JSON
)


# ========== CORS 미들웨어 설정 ==========

# CORS (Cross-Origin Resource Sharing) 미들웨어
# 목적:
#   프론트엔드에서 백엔드 API를 호출할 수 있도록 허용합니다.
#   브라우저의 Same-Origin Policy를 우회합니다.
#
# 왜 필요한가?:
#   프론트엔드: http://localhost:3000
#   백엔드: http://localhost:8000
#   → Origin이 다르므로 브라우저가 기본적으로 요청 차단
#   → CORS 설정으로 허용 필요
#
# 주요 설정:
#   - allow_origins: 허용할 오리진 목록
#     예: ["http://localhost:3000", "http://127.0.0.1:3000"]
#
#   - allow_credentials=True: 쿠키, 인증 헤더 허용
#     - JWT 토큰을 쿠키로 전송하는 경우 필수
#     - 세션 기반 인증 사용 시 필수
#
#   - allow_methods=["*"]: 모든 HTTP 메서드 허용
#     - GET, POST, PUT, DELETE, PATCH, OPTIONS 등
#     - 프로덕션에서는 필요한 메서드만 허용 권장
#
#   - allow_headers=["*"]: 모든 HTTP 헤더 허용
#     - Content-Type, Authorization 등
#     - 프로덕션에서는 필요한 헤더만 허용 권장
#
# 보안 주의사항:
#   - 개발 환경: allow_origins에 localhost 사용
#   - 프로덕션 환경: 실제 프론트엔드 도메인만 허용
#   - "*" 사용 금지 (모든 도메인 허용 = 보안 위험)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # 허용 오리진 (config.py에서 관리)
    allow_credentials=True,  # 쿠키/인증 헤더 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


# ========== 기본 엔드포인트 ==========

@app.get("/health", tags=["Health"])
async def health_check():
    """
    서버 상태 확인 (Health Check)

    목적:
        서버가 정상적으로 실행 중인지 확인하는 엔드포인트입니다.
        로드 밸런서, 모니터링 툴에서 사용합니다.

    사용 시나리오:
        - 배포 후 서버 시작 확인
        - 로드 밸런서의 헬스체크
        - 모니터링 시스템의 Alive 확인
        - CI/CD 파이프라인의 배포 검증

    응답:
        - status: 서버 상태 (항상 "healthy")
        - version: API 버전 (예: "1.0.0")
        - environment: 실행 환경 (예: "development")

    Returns:
        dict: 서버 상태 정보

    예시:
        >>> GET /health
        >>> {
        ...     "status": "healthy",
        ...     "version": "1.0.0",
        ...     "environment": "development"
        ... }
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/", tags=["Root"])
async def root():
    """
    API 루트 엔드포인트 (Welcome)

    목적:
        API의 기본 정보를 제공하는 엔드포인트입니다.
        API 사용 방법과 문서 링크를 안내합니다.

    사용 시나리오:
        - API 접속 시 첫 화면
        - API 정보 확인
        - 문서 링크 안내

    응답:
        - message: 환영 메시지
        - version: API 버전
        - docs: Swagger UI 경로
        - health: 헬스체크 경로

    Returns:
        dict: API 정보

    예시:
        >>> GET /
        >>> {
        ...     "message": "Welcome to DoneDone API",
        ...     "version": "1.0.0",
        ...     "docs": "/docs",
        ...     "health": "/health"
        ... }
    """
    return {
        "message": "Welcome to DoneDone API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# ========== API 라우터 등록 (추후 구현) ==========

# TODO: API 라우터 등록
# Phase 2 이후 API 라우터를 등록할 예정입니다.
#
# 라우터 구조:
#   - auth.router: 인증 관련 (로그인, 회원가입, 토큰 갱신)
#   - products.router: 제품 관리 (등록, 수정, 삭제, 조회)
#   - inventory.router: 재고 조회 (현재고, 매장별 재고)
#   - transactions.router: 트랜잭션 관리 (입고, 출고, 조정)
#   - sync.router: 오프라인 동기화 (미동기 데이터 업로드)
#
# 등록 예시:
#   from app.api.v1 import auth, products, inventory, transactions, sync
#
#   app.include_router(
#       auth.router,
#       prefix=f"{settings.API_V1_PREFIX}/auth",
#       tags=["Auth"]
#   )
#
#   app.include_router(
#       products.router,
#       prefix=f"{settings.API_V1_PREFIX}/products",
#       tags=["Products"]
#   )
#
#   ... (나머지 라우터)
#
# 결과 경로:
#   - POST /api/v1/auth/login
#   - POST /api/v1/auth/register
#   - GET /api/v1/products
#   - POST /api/v1/products
#   - POST /api/v1/transactions/inbound
#   - POST /api/v1/transactions/outbound
#   - POST /api/v1/transactions/adjust


# ========== 개발 서버 실행 ==========

if __name__ == "__main__":
    """
    개발 서버 실행 (python main.py로 직접 실행 시)

    목적:
        python main.py 명령으로 서버를 간편하게 시작합니다.
        개발 중 빠른 테스트를 위한 용도입니다.

    동작:
        - Uvicorn 서버 실행
        - host="0.0.0.0": 모든 네트워크 인터페이스에서 접근 허용
        - port=8000: 8000번 포트에서 실행
        - reload: 개발 환경에서만 자동 재시작 (코드 변경 감지)

    프로덕션에서는 사용하지 않습니다:
        대신 uvicorn 명령으로 직접 실행:
        >>> uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

    개발 환경 실행 방법:
        >>> python backend/app/main.py
        또는
        >>> uvicorn app.main:app --reload

    주의사항:
        - reload=True는 개발 환경에서만 사용 (성능 저하)
        - 프로덕션에서는 Gunicorn + Uvicorn Workers 사용 권장
    """
    import uvicorn
    uvicorn.run(
        "app.main:app",  # 앱 위치 (모듈:객체)
        host="0.0.0.0",  # 모든 IP에서 접근 허용
        port=8000,  # 포트 번호
        reload=settings.ENVIRONMENT == "development"  # 개발 환경에서만 자동 재시작
    )
