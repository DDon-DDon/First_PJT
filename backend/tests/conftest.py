"""
pytest 설정 및 공통 fixtures
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

# 테스트 DB URL (메모리 DB 사용)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 테스트용 비동기 엔진
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

# 테스트용 세션 팩토리
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


@pytest.fixture
async def db_session():
    """테스트용 DB 세션 픽스처"""
    # 테이블 생성
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 세션 생성
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    # 테이블 삭제
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session: AsyncSession):
    """테스트용 HTTP 클라이언트 픽스처"""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ========== 샘플 데이터 Fixtures ==========

@pytest.fixture
def sample_user_data():
    """샘플 사용자 데이터"""
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
    """샘플 매장 데이터"""
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
    """샘플 카테고리 데이터"""
    return {
        "id": uuid4(),
        "code": "TEST",
        "name": "테스트카테고리",
        "sort_order": 1
    }


@pytest.fixture
def sample_product_data(sample_category_data):
    """샘플 제품 데이터"""
    return {
        "id": uuid4(),
        "barcode": "8801234567890",
        "name": "테스트제품",
        "category_id": sample_category_data["id"],
        "safety_stock": 10,
        "is_active": True
    }
