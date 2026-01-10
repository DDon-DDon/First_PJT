import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.models.category import Category
from app.models.store import Store
from app.models.user import User, UserRole
from app.models.user_store import UserStore
from app.api.deps import get_current_user
from app.main import app

@pytest.fixture
async def e2e_setup(db_session, sample_category_data):
    # Setup Category and Store
    cat = Category(**sample_category_data)
    db_session.add(cat)
    
    store = Store(id=uuid4(), code="E2E_STORE", name="E2E Store")
    db_session.add(store)
    
    # Create Admin and Worker
    admin = User(id=uuid4(), email="admin@e2e.com", role=UserRole.ADMIN, name="Admin", password_hash="hash")
    worker = User(id=uuid4(), email="worker@e2e.com", role=UserRole.WORKER, name="Worker", password_hash="hash")
    db_session.add_all([admin, worker])
    
    # Assign Worker
    us = UserStore(user_id=worker.id, store_id=store.id)
    db_session.add(us)
    
    await db_session.commit()
    
    # Expunge to prevent session/greenlet issues during test execution
    db_session.expunge(admin)
    db_session.expunge(worker)
    
    return {"admin": admin, "worker": worker, "store": store, "category": cat}

@pytest.mark.asyncio
async def test_complete_inventory_workflow(client: AsyncClient, db_session: AsyncSession, e2e_setup):
    data = e2e_setup
    admin = data["admin"]
    worker = data["worker"]
    store = data["store"]
    category = data["category"]
    
    # 1. Admin Login (Mock) & Product Registration
    app.dependency_overrides[get_current_user] = lambda: admin
    
    product_payload = {
        "barcode": "E2E-880123",
        "name": "E2E Test Cream",
        "categoryId": str(category.id),
        "safetyStock": 10
    }
    res = await client.post("/api/v1/products", json=product_payload)
    assert res.status_code == 201
    product_data = res.json()
    product_id = product_data["id"]
    barcode = product_data["barcode"]
    
    # 2. Check Initial State
    res = await client.get(f"/api/v1/products/barcode/{barcode}")
    assert res.status_code == 200
    
    # Check Admin Stock View (0)
    res = await client.get(f"/api/v1/inventory/stocks/{product_id}")
    assert res.status_code == 200
    assert res.json()["totalQuantity"] == 0
    
    # 3. Worker Login & Inbound
    app.dependency_overrides[get_current_user] = lambda: worker
    
    inbound_payload = {
        "productId": product_id,
        "storeId": str(store.id),
        "quantity": 50,
        "note": "Initial Stock"
    }
    res = await client.post("/api/v1/transactions/inbound", json=inbound_payload)
    assert res.status_code == 201
    assert res.json()["newStock"] == 50
    
    # 4. Check Stock Status (Worker View)
    res = await client.get("/api/v1/inventory/stocks")
    assert res.status_code == 200
    items = res.json()["items"]
    # Find our product
    target_item = next((i for i in items if i["product"]["id"] == product_id), None)
    assert target_item is not None
    assert target_item["quantity"] == 50
    assert target_item["status"] == "GOOD"
    
    # 5. Outbound
    outbound_payload = {
        "productId": product_id,
        "storeId": str(store.id),
        "quantity": 45,
        "note": "Sales"
    }
    res = await client.post("/api/v1/transactions/outbound", json=outbound_payload)
    assert res.status_code == 201
    res_data = res.json()
    assert res_data["newStock"] == 5
    assert res_data["safetyAlert"] == True
    
    # 6. Insufficient Stock
    fail_payload = {
        "productId": product_id,
        "storeId": str(store.id),
        "quantity": 10 # 5 - 10 < 0
    }
    res = await client.post("/api/v1/transactions/outbound", json=fail_payload)
    assert res.status_code == 400
    
    # 7. Transaction History
    res = await client.get(f"/api/v1/transactions?store_id={store.id}&product_id={product_id}")
    assert res.status_code == 200
    history = res.json()["items"]
    
    # Should have 2 transactions (Inbound, Outbound)
    assert len(history) == 2
    assert history[0]["type"] == "OUTBOUND"
    assert history[0]["quantity"] == -45
    assert history[1]["type"] == "INBOUND"
    assert history[1]["quantity"] == 50
    
    # Cleanup
    app.dependency_overrides.pop(get_current_user)
