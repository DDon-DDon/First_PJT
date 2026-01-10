import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.category import Category
from app.models.user import User, UserRole
from app.main import app
from uuid import uuid4

# Mocking dependency
from app.api.deps import get_current_user

@pytest.mark.asyncio
async def test_get_product_by_barcode_success(client: AsyncClient, db_session: AsyncSession, sample_product_data, sample_category_data):
    # Given: 카테고리와 제품 생성
    category = Category(**sample_category_data)
    db_session.add(category)
    await db_session.flush() # ID 생성을 위해 flush
    
    # sample_product_data는 category_id를 필요로 함. 
    # fixture에서 이미 sample_category_data['id']를 사용하지만, 
    # 실제 DB에 카테고리가 있어야 FK 제약조건을 만족함.
    product = Product(**sample_product_data)
    db_session.add(product)
    await db_session.commit()

    # When: 바코드로 조회
    response = await client.get(f"/api/v1/products/barcode/{product.barcode}")

    # Then: 성공 확인
    assert response.status_code == 200
    data = response.json()
    assert data["barcode"] == product.barcode
    assert data["name"] == product.name

@pytest.mark.asyncio
async def test_get_product_by_barcode_not_found(client: AsyncClient):
    # When: 존재하지 않는 바코드로 조회
    response = await client.get("/api/v1/products/barcode/9999999999999")

    # Then: 404 확인
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_products(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 카테고리와 제품 15개 생성
    category = Category(**sample_category_data)
    db_session.add(category)
    await db_session.flush()

    for i in range(15):
        product = Product(
            barcode=f"88000000000{i:02d}",
            name=f"제품_{i}",
            category_id=category.id,
            safety_stock=10
        )
        db_session.add(product)
    await db_session.commit()

    # When: 목록 조회 (limit=10)
    response = await client.get("/api/v1/products?page=1&limit=10")

    # Then: 페이지네이션 확인
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["pagination"]["total"] == 15
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["totalPages"] == 2

@pytest.mark.asyncio
async def test_list_products_filter(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 카테고리 2개 생성
    cat1 = Category(id=uuid4(), code="CAT1", name="카테고리1", sort_order=1)
    cat2 = Category(id=uuid4(), code="CAT2", name="카테고리2", sort_order=2)
    db_session.add_all([cat1, cat2])
    await db_session.flush()

    # 제품 생성
    p1 = Product(barcode="111", name="검색대상", category_id=cat1.id)
    p2 = Product(barcode="222", name="다른제품", category_id=cat1.id)
    p3 = Product(barcode="333", name="검색대상2", category_id=cat2.id)
    db_session.add_all([p1, p2, p3])
    await db_session.commit()

    # When 1: 이름 검색
    res1 = await client.get("/api/v1/products?search=대상")
    assert res1.status_code == 200
    assert len(res1.json()["items"]) == 2  # 검색대상, 검색대상2

    # When 2: 카테고리 필터
    res2 = await client.get(f"/api/v1/products?category_id={cat1.id}")
    assert res2.status_code == 200
    assert len(res2.json()["items"]) == 2  # p1, p2

@pytest.mark.asyncio
async def test_create_product_admin(client: AsyncClient, db_session: AsyncSession, sample_category_data):
    # Given: 관리자 권한 Mocking
    admin_user = User(id=uuid4(), email="admin@test.com", role=UserRole.ADMIN, name="Admin")
    app.dependency_overrides[get_current_user] = lambda: admin_user

    # 카테고리 생성
    category = Category(**sample_category_data)
    db_session.add(category)
    await db_session.commit()

    payload = {
        "barcode": "NEW12345",
        "name": "신규제품",
        "categoryId": str(category.id),
        "safetyStock": 20
    }

    # When: 제품 생성 요청
    response = await client.post("/api/v1/products", json=payload)

    # Then: 성공 확인
    assert response.status_code == 201
    data = response.json()
    assert data["barcode"] == "NEW12345"
    
    # Clean up
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_create_product_worker_fail(client: AsyncClient):
    # Given: 워커 권한 Mocking
    worker_user = User(id=uuid4(), email="worker@test.com", role=UserRole.WORKER, name="Worker")
    app.dependency_overrides[get_current_user] = lambda: worker_user

    payload = {
        "barcode": "NEW12345",
        "name": "신규제품",
        "categoryId": str(uuid4()),
        "safetyStock": 20
    }

    # When: 제품 생성 요청
    response = await client.post("/api/v1/products", json=payload)

    # Then: 403 Forbidden 확인
    assert response.status_code == 403
    
    # Clean up
    app.dependency_overrides.pop(get_current_user)

@pytest.mark.asyncio
async def test_create_product_duplicate_barcode(client: AsyncClient, db_session: AsyncSession, sample_category_data, sample_product_data):
    # Given: 관리자 권한 & 기존 제품 존재
    admin_user = User(id=uuid4(), email="admin@test.com", role=UserRole.ADMIN, name="Admin")
    app.dependency_overrides[get_current_user] = lambda: admin_user

    category = Category(**sample_category_data)
    db_session.add(category)
    await db_session.flush()
    
    product = Product(**sample_product_data)
    db_session.add(product)
    await db_session.commit()

    # When: 동일 바코드로 생성 시도
    payload = {
        "barcode": sample_product_data["barcode"], # 중복 바코드
        "name": "중복제품",
        "categoryId": str(category.id),
        "safetyStock": 10
    }
    response = await client.post("/api/v1/products", json=payload)

    # Then: 400 또는 409 에러 확인
    assert response.status_code in [400, 409]

    # Clean up
    app.dependency_overrides.pop(get_current_user)
