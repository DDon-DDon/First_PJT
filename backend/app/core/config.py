"""
애플리케이션 설정 관리 (Application Configuration)

파일 역할:
    환경 변수 기반으로 애플리케이션 설정을 관리하는 Pydantic Settings 클래스입니다.
    .env 파일에서 설정을 읽어와 타입 안전하게 검증하고 제공합니다.

패턴:
    - Settings 패턴: 중앙 집중식 설정 관리
    - Environment Variables 패턴: 환경별 설정 분리 (.env 파일)
    - Singleton 패턴: 전역 settings 인스턴스 하나만 생성
    - Type Safety 패턴: Pydantic으로 타입 검증

사용 목적:
    1. 환경별 설정 분리 (development, production)
    2. 민감 정보 보호 (SECRET_KEY, DATABASE_URL 등)
    3. 설정 값 타입 안전성 보장
    4. 코드에서 설정 쉽게 접근 (settings.DATABASE_URL)

작성일: 2025-12-31
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    애플리케이션 설정 관리 클래스

    목적:
        .env 파일에서 환경 변수를 읽어와 애플리케이션 설정을 제공합니다.
        Pydantic을 사용하여 타입 검증 및 기본값 설정을 자동화합니다.

    설정 카테고리:
        1. Application: 프로젝트 기본 정보
        2. Database: 데이터베이스 연결 정보
        3. Security: 인증/암호화 관련 설정
        4. CORS: 프론트엔드 접근 제어

    .env 파일 예시:
        # Application
        PROJECT_NAME="DoneDone API"
        VERSION="1.0.0"
        ENVIRONMENT="development"

        # Database
        DATABASE_URL="postgresql+asyncpg://user:password@localhost/ddon"

        # Security
        SECRET_KEY="your-super-secret-key-here-change-in-production"
        ALGORITHM="HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES=60

        # CORS
        ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"

    사용 예시:
        >>> from app.core.config import settings
        >>>
        >>> # 데이터베이스 URL 가져오기
        >>> print(settings.DATABASE_URL)
        "postgresql+asyncpg://user:password@localhost/ddon"
        >>>
        >>> # 환경 확인
        >>> if settings.ENVIRONMENT == "development":
        ...     print("개발 모드")
        >>>
        >>> # CORS 오리진 리스트 가져오기
        >>> print(settings.allowed_origins_list)
        ["http://localhost:3000", "http://127.0.0.1:3000"]

    주의사항:
        - SECRET_KEY는 절대 하드코딩하지 말 것 (.env에만)
        - 프로덕션 환경에서는 강력한 SECRET_KEY 사용 필수
        - .env 파일은 .gitignore에 추가 (Git에 커밋 금지)
    """

    # ========== Application Settings ==========

    PROJECT_NAME: str = "DoneDone API"
    """
    프로젝트 이름

    용도:
        - FastAPI 문서 제목 (Swagger UI, ReDoc)
        - API 응답 메타데이터
        - 로그 식별자

    기본값: "DoneDone API"
    """

    VERSION: str = "1.0.0"
    """
    API 버전

    용도:
        - API 버전 관리
        - 클라이언트 호환성 체크
        - 문서화

    기본값: "1.0.0"
    """

    API_V1_PREFIX: str = "/api/v1"
    """
    API v1 경로 접두사

    용도:
        - 모든 v1 API 엔드포인트의 기본 경로
        - 예: /api/v1/users, /api/v1/products

    기본값: "/api/v1"
    """

    ENVIRONMENT: str = "development"
    """
    실행 환경

    값:
        - "development": 개발 환경 (SQL 로깅, 디버그 모드)
        - "production": 프로덕션 환경 (최적화, 로깅 최소화)

    용도:
        - SQL 로깅 여부 결정 (session.py)
        - 디버그 모드 설정 (main.py)
        - 에러 응답 상세도 조절

    기본값: "development"
    """

    # ========== Database Settings ==========

    DATABASE_URL: str
    """
    데이터베이스 연결 URL (필수)

    형식:
        postgresql+asyncpg://[user]:[password]@[host]:[port]/[database]

    예시:
        - 로컬: postgresql+asyncpg://postgres:password@localhost:5432/ddon
        - Docker: postgresql+asyncpg://postgres:password@db:5432/ddon

    주의:
        - 필수 필드 (기본값 없음, .env에 반드시 설정)
        - asyncpg 드라이버 사용 (비동기)
        - 프로덕션에서는 강력한 비밀번호 사용
    """
    
    DB_POOL_SIZE: int = 5
    """
    DB 커넥션 풀 크기 (기본 연결 수)
    기본값: 5
    """

    DB_MAX_OVERFLOW: int = 10
    """
    DB 커넥션 풀 오버플로우 허용 수 (최대 연결 수 = POOL_SIZE + MAX_OVERFLOW)
    기본값: 10
    """

    # ========== Security Settings ==========

    SECRET_KEY: str
    """
    JWT 토큰 암호화 키 (필수)

    용도:
        - JWT 액세스 토큰 서명/검증
        - JWT 리프레시 토큰 서명/검증
        - 암호화 작업

    생성 방법:
        >>> import secrets
        >>> secrets.token_urlsafe(32)
        'your-random-secret-key-here'

    주의:
        - 필수 필드 (기본값 없음, .env에 반드시 설정)
        - 절대 하드코딩 금지
        - 프로덕션에서는 최소 32자 이상 랜덤 문자열
        - 유출 시 모든 토큰 무효화되므로 보안 중요
        - .env 파일은 Git에 커밋하지 말 것
    """

    ALGORITHM: str = "HS256"
    """
    JWT 서명 알고리즘

    값:
        - HS256: HMAC + SHA256 (대칭키 암호화)

    용도:
        - JWT 토큰 서명 및 검증 알고리즘

    기본값: "HS256"
    """

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    """
    액세스 토큰 유효 기간 (분)

    용도:
        - JWT 액세스 토큰의 만료 시간 설정
        - 60분 = 1시간 후 토큰 만료

    권장값:
        - 개발: 60~120분 (자주 재로그인 불편)
        - 프로덕션: 15~60분 (보안)

    기본값: 60
    """

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    """
    리프레시 토큰 유효 기간 (일)

    용도:
        - JWT 리프레시 토큰의 만료 시간 설정
        - 7일 후 재로그인 필요

    권장값:
        - 개발: 7~30일
        - 프로덕션: 7~14일

    기본값: 7
    """

    # ========== CORS Settings ==========

    ALLOWED_ORIGINS: str = "http://localhost:3000"
    """
    CORS 허용 오리진 (쉼표로 구분)

    용도:
        - 프론트엔드에서 API 호출 허용
        - 브라우저 CORS 정책 설정

    형식:
        쉼표(,)로 구분된 URL 목록
        예: "http://localhost:3000,http://127.0.0.1:3000,https://example.com"

    주의:
        - 개발: localhost:3000 (Next.js 기본 포트)
        - 프로덕션: 실제 프론트엔드 도메인
        - "*"는 보안상 권장하지 않음

    기본값: "http://localhost:3000"
    """

    @property
    def allowed_origins_list(self) -> List[str]:
        """
        CORS 허용 오리진 리스트 반환

        목적:
            ALLOWED_ORIGINS 문자열을 리스트로 변환합니다.
            FastAPI CORS 미들웨어에서 사용합니다.

        동작:
            "http://localhost:3000,http://127.0.0.1:3000"
            → ["http://localhost:3000", "http://127.0.0.1:3000"]

        Returns:
            List[str]: URL 문자열 리스트 (공백 제거됨)

        예시:
            >>> settings.ALLOWED_ORIGINS = "http://localhost:3000, http://127.0.0.1:3000"
            >>> settings.allowed_origins_list
            ["http://localhost:3000", "http://127.0.0.1:3000"]
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # ========== Pydantic Settings Configuration ==========

    model_config = SettingsConfigDict(
        env_file=".env",  # .env 파일에서 환경 변수 읽기
        env_file_encoding="utf-8",  # 파일 인코딩 (한글 지원)
        case_sensitive=True,  # 대소문자 구분 (DATABASE_URL ≠ database_url)
        extra="allow"  # 정의되지 않은 환경 변수 허용 (미래 확장성)
    )
    """
    Pydantic Settings 설정

    주요 설정:
        - env_file=".env": .env 파일에서 환경 변수 자동 로드
        - env_file_encoding="utf-8": UTF-8 인코딩 (한글 지원)
        - case_sensitive=True: 환경 변수 이름 대소문자 구분
        - extra="allow": 정의되지 않은 환경 변수도 허용

    .env 파일 우선순위:
        1. 실제 환경 변수 (OS 레벨)
        2. .env 파일
        3. 클래스 기본값
    """


# ========== 전역 설정 인스턴스 ==========

settings = Settings()
"""
전역 설정 인스턴스 (Singleton)

용도:
    애플리케이션 전체에서 하나의 설정 인스턴스를 공유합니다.
    .env 파일은 앱 시작 시 한 번만 읽습니다.

사용:
    >>> from app.core.config import settings
    >>> print(settings.DATABASE_URL)

주의:
    - 앱 시작 시 단 한 번만 생성됨
    - .env 파일 변경 시 서버 재시작 필요
    - 런타임 중 설정 값 변경 금지 (불변)
"""
