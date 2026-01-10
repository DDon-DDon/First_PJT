import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4
from datetime import datetime
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
    cat = Category(**sample_category_data)
    db_session.add(cat)
    await db_session.flush()
    
    store = Store(id=uuid4(), code="S1", name="Store1")
    db_session.add(store)
    await db_session.flush()
    
    prod = Product(id=uuid4(), barcode="888", name="Prod", category_id=cat.id, safety_stock=10)
    db_session.add(prod)
    
    worker = User(id=uuid4(), email="w@test.com", role=UserRole.WORKER, name="Worker", password_hash="hash")
    db_session.add(worker)
    
    us = UserStore(user_id=worker.id, store_id=store.id)
    db_session.add(us)
    await db_session.commit()
    
    return {"store": store, "product": prod, "user": worker}

@pytest.mark.asyncio
async def test_sync_batch_success(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    db_session.expunge(data["user"])
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    local_id_1 = str(uuid4())
    local_id_2 = str(uuid4())
    
    payload = {
        "transactions": [
            {
                "localId": local_id_1,
                "type": "INBOUND",
                "productId": str(data["product"].id),
                "storeId": str(data["store"].id),
                "quantity": 30,
                "createdAt": datetime.utcnow().isoformat()
            },
            {
                "localId": local_id_2,
                "type": "OUTBOUND",
                "productId": str(data["product"].id),
                "storeId": str(data["store"].id),
                "quantity": 10,
                "createdAt": datetime.utcnow().isoformat()
            }
        ]
    }
    
    res = await client.post("/api/v1/sync/transactions", json=payload)
    assert res.status_code == 200
    res_data = res.json()
    assert len(res_data["synced"]) == 2
    assert len(res_data["failed"]) == 0
    
    # Verify Stock: 30 - 10 = 20
    stmt = select(CurrentStock).where(CurrentStock.product_id == data["product"].id)
    stock = (await db_session.execute(stmt)).scalar_one()
    assert stock.quantity == 20
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_sync_duplicate_ignore(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    db_session.expunge(data["user"])
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    local_id = str(uuid4())
    tx_data = {
        "localId": local_id,
        "type": "INBOUND",
        "productId": str(data["product"].id),
        "storeId": str(data["store"].id),
        "quantity": 10,
        "createdAt": datetime.utcnow().isoformat()
    }
    
    # First sync
    res1 = await client.post("/api/v1/sync/transactions", json={"transactions": [tx_data]})
    assert res1.status_code == 200
    assert len(res1.json()["synced"]) == 1
    
    # Second sync (same local_id)
    res2 = await client.post("/api/v1/sync/transactions", json={"transactions": [tx_data]})
    assert res2.status_code == 200
    res_data = res2.json()
    assert len(res_data["synced"]) == 1
    assert len(res_data["failed"]) == 0
    
    # Verify stock is 10 (not 20)
    stmt = select(CurrentStock).where(CurrentStock.product_id == data["product"].id)
    stock = (await db_session.execute(stmt)).scalar_one()
    assert stock.quantity == 10
    
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_sync_partial_fail(client: AsyncClient, db_session: AsyncSession, setup_data):
    data = setup_data
    # Expunge user to prevent MissingGreenlet error when accessing expired object after rollback
    db_session.expunge(data["user"])
    app.dependency_overrides[get_current_user] = lambda: data["user"]
    
    local_1 = str(uuid4())
    local_2 = str(uuid4())
    local_3 = str(uuid4())
    
    payload = {
        "transactions": [
            {
                "localId": local_1, "type": "INBOUND", "productId": str(data["product"].id),
                "storeId": str(data["store"].id), "quantity": 10, "createdAt": datetime.utcnow().isoformat()
            },
            {
                "localId": local_2, "type": "OUTBOUND", "productId": str(data["product"].id),
                "storeId": str(data["store"].id), "quantity": 20, "createdAt": datetime.utcnow().isoformat()
            },
            {
                "localId": local_3, "type": "INBOUND", "productId": str(data["product"].id),
                "storeId": str(data["store"].id), "quantity": 5, "createdAt": datetime.utcnow().isoformat()
            }
        ]
    }
    
    res = await client.post("/api/v1/sync/transactions", json=payload)
    assert res.status_code == 200
    res_data = res.json()
    
    print(f"DEBUG: Synced: {res_data['synced']}")
    print(f"DEBUG: Failed: {res_data['failed']}")
    
    synced_ids = [item["localId"] for item in res_data["synced"]]
    failed_ids = [item["localId"] for item in res_data["failed"]]
    
    assert local_1 in synced_ids
    assert local_3 in synced_ids
    assert local_2 in failed_ids
    
    assert len(res_data["synced"]) == 2
    assert len(res_data["failed"]) == 1
    
    # Verify stock: 10 + 5 = 15
    stmt = select(CurrentStock).where(CurrentStock.product_id == data["product"].id)
    stock = (await db_session.execute(stmt)).scalar_one()
    assert stock.quantity == 15
    
    app.dependency_overrides.pop(get_current_user)
