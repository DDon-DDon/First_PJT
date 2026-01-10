import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.models.product import Product
from app.models.store import Store
from app.models.category import Category
from app.models.stock import CurrentStock
from app.models.user import User, UserRole
from app.models.user_store import UserStore
from app.api.deps import get_current_user
from app.main import app

@pytest.fixture
async def setup_data(db_session, sample_category_data):
    # Category
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()
    
    # Store
    store = Store(id=uuid4(), code="S1", name="Store1")
    db_session.add(store)
    await db_session.flush()
    
    # Product
    prod = Product(id=uuid4(), barcode="888", name="Prod", category_id=cat.id, safety_stock=10)
    db_session.add(prod)
    await db_session.commit()
    
    # User (Worker)
    worker = User(id=uuid4(), email="w@test.com", role=UserRole.WORKER, name="Worker", password_hash="hash")
    db_session.add(worker)
    
    # Assign Worker to Store
    us = UserStore(user_id=worker.id, store_id=store.id)
    db_session.add(us)
    await db_session.commit()
    
    return {"store": store, "product": prod, "user": worker}

@pytest.mark.asyncio
async def test_inbound_success(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    payload = {
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": 30,
        "note": "Inbound"
    }
    
    res = await client.post("/api/v1/transactions/inbound", json=payload)
    assert res.status_code == 201
    res_data = res.json()
    assert res_data["quantity"] == 30
    assert res_data["newStock"] == 30
    assert res_data["type"] == "INBOUND"
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_inbound_accumulate(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    # Initial Stock 10
    stock = CurrentStock(product_id=data["product"].id, store_id=data["store"].id, quantity=10)
    db_session.add(stock)
    await db_session.commit()
    
    payload = {
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": 20
    }
    
    res = await client.post("/api/v1/transactions/inbound", json=payload)
    assert res.status_code == 201
    assert res.json()["newStock"] == 30 # 10 + 20
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_outbound_success(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    # Initial Stock 30
    stock = CurrentStock(product_id=data["product"].id, store_id=data["store"].id, quantity=30)
    db_session.add(stock)
    await db_session.commit()
    
    payload = {
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": 10
    }
    
    res = await client.post("/api/v1/transactions/outbound", json=payload)
    assert res.status_code == 201
    res_data = res.json()
    assert res_data["quantity"] == -10 # Stored as negative
    assert res_data["newStock"] == 20 # 30 - 10
    assert res_data["type"] == "OUTBOUND"
    assert res_data["safetyAlert"] == False # 20 >= 10
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_outbound_insufficient_stock(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    # Initial Stock 5
    stock = CurrentStock(product_id=data["product"].id, store_id=data["store"].id, quantity=5)
    db_session.add(stock)
    await db_session.commit()
    
    payload = {
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": 10 # Request > Stock
    }
    
    res = await client.post("/api/v1/transactions/outbound", json=payload)
    assert res.status_code == 400
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_outbound_safety_alert(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    # Initial Stock 12, Safety 10
    stock = CurrentStock(product_id=data["product"].id, store_id=data["store"].id, quantity=12)
    db_session.add(stock)
    await db_session.commit()
    
    payload = {
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": 5
    }
    
    # Result: 12 - 5 = 7. 7 < 10. Alert!
    res = await client.post("/api/v1/transactions/outbound", json=payload)
    assert res.status_code == 201
    assert res.json()["safetyAlert"] == True
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_adjust_stock(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    # Initial Stock 10
    stock = CurrentStock(product_id=data["product"].id, store_id=data["store"].id, quantity=10)
    db_session.add(stock)
    await db_session.commit()
    
    payload = {
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": -2,
        "reason": "EXPIRED"
    }
    
    res = await client.post("/api/v1/transactions/adjust", json=payload)
    assert res.status_code == 201
    res_data = res.json()
    assert res_data["quantity"] == -2
    assert res_data["newStock"] == 8
    assert res_data["reason"] == "EXPIRED"
    assert res_data["type"] == "ADJUST"
    
    app.dependency_overrides.pop(get_current_user)
