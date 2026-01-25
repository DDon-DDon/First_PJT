"""
E2E 테스트 전용 fixtures

다이어그램 기반 시나리오 테스트를 위한 공통 설정:
- admin_client: ADMIN 권한 클라이언트
- worker_client: WORKER 권한 클라이언트  
- seeded_data: 기본 테스트 데이터셋
"""
import pytest
from typing import AsyncGenerator
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.api.deps import get_current_user
from app.models.user import User, UserRole
from app.models.store import Store
from app.models.category import Category
from app.models.product import Product
from app.models.user_store import UserStore
from app.models.stock import CurrentStock


@pytest.fixture
async def seeded_data(db_session: AsyncSession):
    """
    E2E 테스트용 기본 데이터 시드
    
    생성되는 데이터:
    - Category: 스킨케어 (SK)
    - Store: 강남점, 홍대점
    - Product: 수분크림 (barcode: 8801234567890)
    - User: admin@test.com (ADMIN), worker@test.com (WORKER)
    - UserStore: worker → 강남점 배정
    - CurrentStock: 수분크림@강남점 = 50개
    """
    # 1. 카테고리
    category = Category(
        id=uuid4(),
        code="SK",
        name="스킨케어",
        sort_order=1
    )
    db_session.add(category)
    
    # 2. 매장
    store_gangnam = Store(
        id=uuid4(),
        code="STORE-001",
        name="강남점",
        address="서울시 강남구",
        is_active=True
    )
    store_hongdae = Store(
        id=uuid4(),
        code="STORE-002", 
        name="홍대점",
        address="서울시 마포구",
        is_active=True
    )
    db_session.add_all([store_gangnam, store_hongdae])
    
    # 3. 제품
    product = Product(
        id=uuid4(),
        barcode="8801234567890",
        name="수분크림 50ml",
        category_id=category.id,
        safety_stock=10,
        is_active=True
    )
    db_session.add(product)
    
    # 4. 사용자
    admin = User(
        id=uuid4(),
        email="admin@test.com",
        password_hash="$2b$12$hashed",  # 실제 해시 아님, 테스트용
        name="관리자",
        role=UserRole.ADMIN,
        is_active=True
    )
    worker = User(
        id=uuid4(),
        email="worker@test.com",
        password_hash="$2b$12$hashed",
        name="작업자",
        role=UserRole.WORKER,
        is_active=True
    )
    db_session.add_all([admin, worker])
    
    # 5. 매장 배정 (worker → 강남점만)
    user_store = UserStore(
        user_id=worker.id,
        store_id=store_gangnam.id
    )
    db_session.add(user_store)
    
    # 6. 초기 재고 (강남점에 50개)
    stock = CurrentStock(
        product_id=product.id,
        store_id=store_gangnam.id,
        quantity=50
    )
    db_session.add(stock)
    
    await db_session.commit()
    
    # Expunge to prevent greenlet issues
    for obj in [category, store_gangnam, store_hongdae, product, admin, worker]:
        db_session.expunge(obj)
    
    return {
        "category": category,
        "store_gangnam": store_gangnam,
        "store_hongdae": store_hongdae,
        "product": product,
        "admin": admin,
        "worker": worker,
    }


@pytest.fixture
async def admin_client(client: AsyncClient, seeded_data) -> AsyncGenerator[AsyncClient, None]:
    """ADMIN 권한으로 설정된 클라이언트"""
    admin = seeded_data["admin"]
    
    app.dependency_overrides[get_current_user] = lambda: admin
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
async def worker_client(client: AsyncClient, seeded_data) -> AsyncGenerator[AsyncClient, None]:
    """WORKER 권한으로 설정된 클라이언트"""
    worker = seeded_data["worker"]
    
    app.dependency_overrides[get_current_user] = lambda: worker
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def unauthenticated_client(client: AsyncClient) -> AsyncClient:
    """인증 없는 클라이언트 (의존성 오버라이드 없음)"""
    # 만약 get_current_user 오버라이드가 있다면 제거
    app.dependency_overrides.pop(get_current_user, None)
    return client
