import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.models.stock import CurrentStock
from app.models.product import Product
from app.models.store import Store
from app.models.category import Category
from app.models.user import User, UserRole
from app.models.user_store import UserStore
from app.api.deps import get_current_user
from app.main import app
from app.services.inventory import get_stock_status

# Task 1: Unit Test for Logic
def test_logic_get_stock_status():
    assert get_stock_status(5, 10) == "LOW"      # 5 < 10
    assert get_stock_status(10, 10) == "NORMAL"  # 10 <= 10 < 20
    assert get_stock_status(15, 10) == "NORMAL"  # 15 < 20
    assert get_stock_status(20, 10) == "GOOD"    # 20 >= 20
    assert get_stock_status(30, 10) == "GOOD"

@pytest.mark.asyncio
async def test_list_stocks_worker(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 매장 2개, 제품 1개, 각 매장에 재고 있음
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()

    store1 = Store(id=uuid4(), code="S1", name="Store1")
    store2 = Store(id=uuid4(), code="S2", name="Store2")
    db_session.add_all([store1, store2])
    await db_session.flush()

    prod = Product(id=uuid4(), barcode="888", name="Prod", category_id=cat.id, safety_stock=10)
    db_session.add(prod)
    await db_session.flush()

    # Store1: 5개 (LOW), Store2: 30개 (GOOD)
    stock1 = CurrentStock(product_id=prod.id, store_id=store1.id, quantity=5)
    stock2 = CurrentStock(product_id=prod.id, store_id=store2.id, quantity=30)
    db_session.add_all([stock1, stock2])
    
    # Worker는 Store1에만 배정
    worker = User(id=uuid4(), email="w@test.com", role=UserRole.WORKER, name="Worker", password_hash="hash")
    db_session.add(worker)
    
    # UserStore 관계 생성 (Phase 1 모델 필요)
    # app/models/user_store.py를 확인해야 함. Assuming UserStore exists.
    # 만약 UserStore가 없다면 User.stores relationship을 통해 추가
    # models/user.py를 확인해봐야 겠지만, UserStore 테이블은 존재함 (ERD)
    
    # UserStore 직접 추가 or relationship 사용
    # 여기서는 UserStore 직접 추가 가정 (다대다)
    user_store = UserStore(user_id=worker.id, store_id=store1.id)
    db_session.add(user_store)
    
    await db_session.commit()

    # Mock Current User
    app.dependency_overrides[get_current_user] = lambda: worker

    # When: 재고 조회
    response = await client.get("/api/v1/inventory/stocks")

    # Then: Store1의 재고만 보여야 함
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    assert len(items) == 1
    assert items[0]["store"]["code"] == "S1"
    assert items[0]["status"] == "LOW"

    # Clean up
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_list_stocks_admin(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 매장 2개, 제품 1개
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()

    store1 = Store(id=uuid4(), code="S1", name="Store1")
    store2 = Store(id=uuid4(), code="S2", name="Store2")
    db_session.add_all([store1, store2])
    await db_session.flush()

    prod = Product(id=uuid4(), barcode="888", name="Prod", category_id=cat.id, safety_stock=10)
    db_session.add(prod)
    await db_session.flush()

    stock1 = CurrentStock(product_id=prod.id, store_id=store1.id, quantity=5)
    stock2 = CurrentStock(product_id=prod.id, store_id=store2.id, quantity=30)
    db_session.add_all([stock1, stock2])
    await db_session.commit()

    # Admin
    admin = User(id=uuid4(), email="a@test.com", role=UserRole.ADMIN, name="Admin", password_hash="hash")
    app.dependency_overrides[get_current_user] = lambda: admin

    # When 1: 전체 조회 (Admin은 제한 없음, 혹은 다 보임)
    # 구현에 따라 Admin은 store_id 없으면 전체? or none?
    # 지시서: "ADMIN: 모든 매장, 또는 특정 매장을 선택하여 조회 가능"
    res1 = await client.get("/api/v1/inventory/stocks")
    assert res1.status_code == 200
    assert len(res1.json()["items"]) == 2

    # When 2: 특정 매장 필터
    res2 = await client.get(f"/api/v1/inventory/stocks?store_id={store2.id}")
    assert res2.status_code == 200
    data2 = res2.json()["items"]
    assert len(data2) == 1
    assert data2[0]["store"]["code"] == "S2"

    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_list_stocks_status_filter(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 같은 매장, 제품 3개 (LOW, NORMAL, GOOD)
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()
    
    store = Store(id=uuid4(), code="S1", name="Store1")
    db_session.add(store)
    await db_session.flush()

    # Safety Stock = 10
    # LOW: 5, NORMAL: 15, GOOD: 25
    p1 = Product(id=uuid4(), barcode="1", name="Low", category_id=cat.id, safety_stock=10)
    p2 = Product(id=uuid4(), barcode="2", name="Norm", category_id=cat.id, safety_stock=10)
    p3 = Product(id=uuid4(), barcode="3", name="Good", category_id=cat.id, safety_stock=10)
    db_session.add_all([p1, p2, p3])
    await db_session.flush()

    s1 = CurrentStock(product_id=p1.id, store_id=store.id, quantity=5)
    s2 = CurrentStock(product_id=p2.id, store_id=store.id, quantity=15)
    s3 = CurrentStock(product_id=p3.id, store_id=store.id, quantity=25)
    db_session.add_all([s1, s2, s3])
    await db_session.commit()

    admin = User(id=uuid4(), email="a@test.com", role=UserRole.ADMIN, name="Admin")
    app.dependency_overrides[get_current_user] = lambda: admin

    # When: status=LOW
    res = await client.get("/api/v1/inventory/stocks?status=LOW")
    
    # Then
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) == 1
    assert items[0]["product"]["name"] == "Low"
    assert items[0]["status"] == "LOW"

    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_get_product_stock_detail(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 매장 2개, 제품 1개
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()
    
    store1 = Store(id=uuid4(), code="S1", name="Store1")
    store2 = Store(id=uuid4(), code="S2", name="Store2")
    db_session.add_all([store1, store2])
    await db_session.flush()

    prod = Product(id=uuid4(), barcode="888", name="Prod", category_id=cat.id, safety_stock=10)
    db_session.add(prod)
    await db_session.flush()

    s1 = CurrentStock(product_id=prod.id, store_id=store1.id, quantity=5)
    s2 = CurrentStock(product_id=prod.id, store_id=store2.id, quantity=30)
    db_session.add_all([s1, s2])
    await db_session.commit()

    admin = User(id=uuid4(), email="a@test.com", role=UserRole.ADMIN, name="Admin", password_hash="hash")
    app.dependency_overrides[get_current_user] = lambda: admin

    # When
    res = await client.get(f"/api/v1/inventory/stocks/{prod.id}")

    # Then
    assert res.status_code == 200
    data = res.json()
    assert data["product"]["name"] == "Prod"
    assert len(data["stocks"]) == 2
    assert data["totalQuantity"] == 35 # 5 + 30

    app.dependency_overrides.pop(get_current_user)
