"""
pytest 설정 및 공통 fixtures

파일 역할:
    모든 테스트에서 공통으로 사용하는 pytest fixtures를 정의합니다.
    DB 세션, HTTP 클라이언트, 샘플 데이터를 제공합니다.

패턴:
    - Fixture 패턴: 테스트 준비 및 정리를 자동화
    - Dependency Injection: 테스트 함수에 필요한 의존성 주입
    - Test Isolation: 각 테스트마다 독립적인 DB 환경 제공

작성일: 2026-01-01
TDD: Phase 1.1 - RED 단계에서 작성
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from uuid import uuid4

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings

# ========== 테스트 DB 설정 ==========

# 테스트 DB URL (인메모리 SQLite)
# 장점:
#   1. 빠름: 디스크 I/O 없이 메모리에서 동작
#   2. 격리: 각 테스트마다 독립적인 DB
#   3. 설정 불필요: SQLite 내장, 설치 없음
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 테스트용 비동기 엔진
# echo=False: SQL 로그 출력 안 함 (테스트 속도 향상)
# future=True: SQLAlchemy 2.0 스타일 사용
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,  # SQL 디버깅이 필요하면 True로 변경
    future=True
)

# 테스트용 세션 팩토리
# expire_on_commit=False: 커밋 후에도 객체 접근 가능
# autocommit=False: 명시적 커밋 필요
# autoflush=False: 명시적 flush 필요
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# ========== DB 세션 Fixture ==========

@pytest.fixture
async def db_session():
    """
    테스트용 DB 세션 fixture

    목적:
        각 테스트마다 독립적인 DB 환경을 제공합니다.
        테스트 전 테이블 생성, 테스트 후 롤백 및 테이블 삭제로
        완전한 테스트 격리를 보장합니다.

    작동 순서:
        1. 테이블 생성 (Base.metadata.create_all)
        2. 세션 생성 및 테스트에 제공 (yield)
        3. 테스트 종료 후 롤백 (변경사항 취소)
        4. 테이블 삭제 (다음 테스트를 위해 깨끗하게)

    왜 매번 테이블을 생성/삭제하나요?
        - 완전한 격리: 이전 테스트의 영향 없음
        - 일관성: 항상 동일한 초기 상태에서 시작
        - 안전성: 테스트 실패해도 다음 테스트에 영향 없음

    사용 예시:
        >>> @pytest.mark.asyncio
        >>> async def test_create_user(db_session):
        ...     user = User(email="test@example.com", ...)
        ...     db_session.add(user)
        ...     await db_session.commit()
        ...     # 테스트 종료 후 자동으로 롤백 및 테이블 삭제

    Yields:
        AsyncSession: SQLAlchemy 비동기 세션 객체

    주의사항:
        - pytest.ini에 `asyncio_mode = auto` 설정 필요
        - 이 fixture는 function scope (테스트마다 실행)
    """
    # 1. 테이블 생성
    # run_sync: 동기 함수를 비동기 컨텍스트에서 실행
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. 세션 생성 및 제공
    async with TestSessionLocal() as session:
        yield session  # 테스트 함수로 전달
        # 테스트 종료 후 이 아래 코드 실행
        await session.rollback()  # 모든 변경사항 취소

    # 3. 테이블 삭제 (다음 테스트를 위해 깨끗하게)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ========== HTTP 클라이언트 Fixture ==========

@pytest.fixture
async def client(db_session: AsyncSession):
    """
    테스트용 HTTP 클라이언트 fixture

    목적:
        FastAPI 엔드포인트를 테스트하기 위한 HTTP 클라이언트를 제공합니다.
        실제 서버를 띄우지 않고도 API 테스트 가능합니다.

    작동 방식:
        1. FastAPI의 get_db 의존성을 테스트 DB 세션으로 교체
        2. AsyncClient 생성 (HTTPX 라이브러리)
        3. 테스트에서 API 호출 가능
        4. 테스트 종료 후 의존성 원상복구

    왜 의존성을 교체하나요?
        - 프로덕션 DB 대신 테스트 DB 사용
        - 테스트 격리 보장
        - 실제 DB 오염 방지

    사용 예시:
        >>> @pytest.mark.asyncio
        >>> async def test_login(client):
        ...     response = await client.post("/auth/login", json={
        ...         "email": "test@example.com",
        ...         "password": "test123"
        ...     })
        ...     assert response.status_code == 200

    Args:
        db_session: db_session fixture로부터 주입

    Yields:
        AsyncClient: HTTPX 비동기 HTTP 클라이언트

    주의사항:
        - 실제 서버를 띄우지 않음 (메모리 내에서 실행)
        - base_url은 "http://test" (실제로 사용되지 않음)
    """
    # 의존성 교체: get_db → 테스트 DB 세션 반환
    async def override_get_db():
        """테스트용 DB 세션 제공 함수"""
        yield db_session

    # FastAPI 의존성 오버라이드 등록
    app.dependency_overrides[get_db] = override_get_db

    # HTTP 클라이언트 생성 및 제공
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac  # 테스트 함수로 전달

    # 테스트 종료 후 의존성 원상복구
    app.dependency_overrides.clear()


# ========== 샘플 데이터 Fixtures ==========
# 테스트에서 반복적으로 사용하는 데이터를 fixture로 제공
# 장점:
#   1. 코드 중복 제거
#   2. 일관된 테스트 데이터
#   3. 수정 시 한 곳만 변경하면 됨

@pytest.fixture
def sample_user_data():
    """
    샘플 사용자 데이터

    목적:
        User 모델 테스트에서 사용할 기본 사용자 데이터를 제공합니다.

    Returns:
        dict: 사용자 생성에 필요한 모든 필드

    사용 예시:
        >>> async def test_create_user(db_session, sample_user_data):
        ...     user = User(**sample_user_data)
        ...     db_session.add(user)
        ...     await db_session.commit()
    """
    return {
        "id": uuid4(),
        "email": "test@example.com",
        "password": "test123",
        "name": "테스트유저",
        "role": "WORKER",
        "is_active": True
    }


@pytest.fixture
def sample_store_data():
    """
    샘플 매장 데이터

    목적:
        Store 모델 테스트에서 사용할 기본 매장 데이터를 제공합니다.

    Returns:
        dict: 매장 생성에 필요한 모든 필드

    사용 예시:
        >>> async def test_create_store(db_session, sample_store_data):
        ...     store = Store(**sample_store_data)
        ...     db_session.add(store)
        ...     await db_session.commit()
    """
    return {
        "id": uuid4(),
        "code": "STORE-TEST",
        "name": "테스트매장",
        "address": "서울시 강남구",
        "phone": "02-1234-5678",
        "is_active": True
    }


@pytest.fixture
def sample_category_data():
    """
    샘플 카테고리 데이터

    목적:
        Category 모델 테스트에서 사용할 기본 카테고리 데이터를 제공합니다.

    Returns:
        dict: 카테고리 생성에 필요한 모든 필드

    사용 예시:
        >>> async def test_create_category(db_session, sample_category_data):
        ...     category = Category(**sample_category_data)
        ...     db_session.add(category)
        ...     await db_session.commit()
    """
    return {
        "id": uuid4(),
        "code": "TEST",
        "name": "테스트카테고리",
        "sort_order": 1
    }


@pytest.fixture
def sample_product_data(sample_category_data):
    """
    샘플 제품 데이터

    목적:
        Product 모델 테스트에서 사용할 기본 제품 데이터를 제공합니다.

    Args:
        sample_category_data: 카테고리 fixture로부터 주입
            제품은 카테고리에 속하므로 category_id 필요

    Returns:
        dict: 제품 생성에 필요한 모든 필드

    사용 예시:
        >>> async def test_create_product(db_session, sample_product_data):
        ...     product = Product(**sample_product_data)
        ...     db_session.add(product)
        ...     await db_session.commit()

    주의:
        이 fixture를 사용하려면 먼저 Category를 DB에 생성해야 합니다.
        (FK 제약조건 때문)
    """
    return {
        "id": uuid4(),
        "barcode": "8801234567890",
        "name": "테스트제품",
        "category_id": sample_category_data["id"],
        "safety_stock": 10,
        "is_active": True
    }


# ========== 추가 Fixtures (추후 확장) ==========
# Phase 2 이후 인증 관련 fixtures 추가 예정:
#
# @pytest.fixture
# async def auth_user(db_session, sample_user_data):
#     """인증된 사용자 fixture"""
#     # 사용자 생성 및 토큰 반환
#     pass
#
# @pytest.fixture
# async def admin_user(db_session):
#     """관리자 사용자 fixture"""
#     # ADMIN 역할 사용자 생성
#     pass
#
# @pytest.fixture
# def auth_headers(auth_user):
#     """인증 헤더 fixture"""
#     # Bearer token 헤더 반환
#     return {"Authorization": f"Bearer {auth_user.token}"}
