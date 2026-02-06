import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.inventory import get_current_stocks
from app.models.store import Store
from app.models.category import Category
from app.models.product import Product
from app.models.stock import CurrentStock
from app.core.query_analyzer import QueryCounter

@pytest.mark.asyncio
async def test_stocks_list_n_plus_one(db_session: AsyncSession):
    """
    N+1 문제 검증 테스트: 재고 목록 조회
    
    데이터가 5개일 때와 10개일 때 쿼리 개수가 동일해야 한다 (또는 선형적으로 증가하지 않아야 한다).
    기대 쿼리:
    1. Count 쿼리
    2. 목록 조회 쿼리 (JOIN 포함)
    (총 2회 예상)
    """
    # 1. Store 생성
    store = Store(
        id=uuid.uuid4(),
        code="NP-STORE",
        name="N+1 Test Store",
        is_active=True
    )
    db_session.add(store)
    
    # 2. Category 생성
    category = Category(
        id=uuid.uuid4(),
        code="NP-CAT",
        name="N+1 Test Category",
        sort_order=1
    )
    db_session.add(category)
    await db_session.flush() # ID 참조를 위해 flush

    # 3. Product & Stock 생성 (5개)
    for i in range(5):
        product = Product(
            id=uuid.uuid4(),
            barcode=f"880000000000{i}",
            name=f"Product {i}",
            category_id=category.id,
            safety_stock=10,
            is_active=True
        )
        db_session.add(product)
        
        stock = CurrentStock(
            product_id=product.id,
            store_id=store.id,
            quantity=100 + i
        )
        db_session.add(stock)

    await db_session.commit() # 커밋하여 데이터 저장

    # 4. 조회 및 쿼리 카운트 측정
    # QueryCounter는 engine에 이벤트를 바인딩하므로 session.bind(engine)을 사용
    # 주의: AsyncSession의 bind는 connectable(engine)임.
    
    # N=5 조회
    async with QueryCounter(db_session) as counter:
        items, total = await get_current_stocks(
            db_session,
            store_id=store.id,
            page=1,
            limit=10
        )
    
    query_count_5 = counter.count
    # print(f"Queries for 5 items: {query_count_5}")
    
    # 검증:
    # - 데이터가 로드되었는지 확인
    assert len(items) == 5
    assert total == 5
    # - Product와 Store가 로드되었는지 확인 (세션이 닫혀도 접근 가능해야 eager loading 성공)
    #   (테스트 세션 특성상 lazy load가 발생할 수 있으나, N+1 문제라면 여기서 추가 쿼리가 발생할 것임)
    #   하지만 QueryCounter 블록 밖이므로 추가 쿼리는 카운트되지 않음.
    #   중요한 건 메인 로직 실행 중(위 블록 안) 쿼리 개수임.
    
    # Eager Loading이 적용되었다면 쿼리는 1~2개여야 함 (Count + Select)
    # 만약 N+1이라면 5 + 2 = 7개 이상일 것.
    assert query_count_5 <= 3, f"Too many queries! Expected <= 3, got {query_count_5}"

    # 5. 데이터 추가 (10개로 증가)
    for i in range(5, 10):
        product = Product(
            id=uuid.uuid4(),
            barcode=f"880000000000{i}",
            name=f"Product {i}",
            category_id=category.id,
            safety_stock=10,
            is_active=True
        )
        db_session.add(product)
        stock = CurrentStock(
            product_id=product.id,
            store_id=store.id,
            quantity=100 + i
        )
        db_session.add(stock)
    await db_session.commit()

    # N=10 조회
    async with QueryCounter(db_session) as counter_10:
        items_10, total_10 = await get_current_stocks(
            db_session,
            store_id=store.id,
            page=1,
            limit=20
        )
    
    query_count_10 = counter_10.count
    # print(f"Queries for 10 items: {query_count_10}")

    assert len(items_10) == 10
    # 데이터가 늘어도 쿼리 개수는 같아야 함 (O(1))
    assert query_count_10 == query_count_5, \
        f"Query count increased! N=5: {query_count_5}, N=10: {query_count_10}"
