import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.models.product import Product
from app.models.store import Store
from app.models.category import Category
from app.models.stock import CurrentStock
from app.models.user import User, UserRole
from app.api.deps import get_current_user
from app.main import app

@pytest.fixture
async def admin_data(db_session, sample_category_data):
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()
    
    store = Store(id=uuid4(), code="S1", name="Store1")
    db_session.add(store)
    await db_session.flush()
    
    # Safety Stock 10
    p1 = Product(id=uuid4(), barcode="1", name="LowP", category_id=cat.id, safety_stock=10)
    p2 = Product(id=uuid4(), barcode="2", name="GoodP", category_id=cat.id, safety_stock=10)
    db_session.add_all([p1, p2])
    await db_session.flush()
    
    # Low Stock (5)
    s1 = CurrentStock(product_id=p1.id, store_id=store.id, quantity=5)
    # Good Stock (20)
    s2 = CurrentStock(product_id=p2.id, store_id=store.id, quantity=20)
    db_session.add_all([s1, s2])
    
    admin = User(id=uuid4(), email="admin@test.com", role=UserRole.ADMIN, name="Admin", password_hash="hash")
    db_session.add(admin)
    
    worker = User(id=uuid4(), email="worker@test.com", role=UserRole.WORKER, name="Worker", password_hash="hash")
    db_session.add(worker)
    
    await db_session.commit()
    
    return {"admin": admin, "worker": worker, "low_product": p1}

@pytest.mark.asyncio
async def test_get_low_stock_admin(client: AsyncClient, db_session: AsyncSession, admin_data):
    data = admin_data
    # Use detached user to avoid Greenlet error
    db_session.expunge(data["admin"])
    app.dependency_overrides[get_current_user] = lambda: data["admin"]
    
    res = await client.get("/api/v1/alerts/low-stock")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["product"]["name"] == "LowP"
    assert items[0]["shortage"] == 5 # 10 - 5
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_get_low_stock_worker_forbidden(client: AsyncClient, db_session: AsyncSession, admin_data):
    data = admin_data
    db_session.expunge(data["worker"])
    app.dependency_overrides[get_current_user] = lambda: data["worker"]
    
    res = await client.get("/api/v1/alerts/low-stock")
    assert res.status_code == 403
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_export_low_stock(client: AsyncClient, db_session: AsyncSession, admin_data):
    data = admin_data
    db_session.expunge(data["admin"])
    app.dependency_overrides[get_current_user] = lambda: data["admin"]
    
    res = await client.get("/api/v1/exports/low-stock")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    app.dependency_overrides.pop(get_current_user)
