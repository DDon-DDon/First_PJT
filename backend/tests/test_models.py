"""
🔴 RED: SQLAlchemy 모델 테스트

테스트 먼저 작성 → 구현은 나중에
"""
import pytest
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import select

from app.models.user import User, UserRole
from app.models.store import Store
from app.models.category import Category
from app.models.product import Product
from app.models.transaction import InventoryTransaction, TransactionType, AdjustReason
from app.models.stock import CurrentStock


class TestUserModel:
    """User 모델 테스트"""

    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """사용자 생성 테스트"""
        user = User(
            id=uuid4(),
            email="test@example.com",
            password_hash="hashed_password",
            name="테스트유저",
            role=UserRole.WORKER,
            is_active=True,
            created_at=datetime.utcnow()
        )

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.role == UserRole.WORKER
        assert user.is_active is True

    @pytest.mark.asyncio
    async def test_user_default_role(self, db_session):
        """사용자 기본 역할은 WORKER"""
        user = User(
            id=uuid4(),
            email="worker@example.com",
            password_hash="hashed",
            name="작업자",
            created_at=datetime.utcnow()
        )

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.role == UserRole.WORKER

    @pytest.mark.asyncio
    async def test_user_email_unique(self, db_session):
        """이메일은 유니크해야 함"""
        user1 = User(
            id=uuid4(),
            email="duplicate@example.com",
            password_hash="hash1",
            name="유저1",
            created_at=datetime.utcnow()
        )

        user2 = User(
            id=uuid4(),
            email="duplicate@example.com",
            password_hash="hash2",
            name="유저2",
            created_at=datetime.utcnow()
        )

        db_session.add(user1)
        await db_session.commit()

        db_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()


class TestStoreModel:
    """Store 모델 테스트"""

    @pytest.mark.asyncio
    async def test_create_store(self, db_session):
        """매장 생성 테스트"""
        store = Store(
            id=uuid4(),
            code="STORE-001",
            name="강남1호점",
            address="서울시 강남구",
            phone="02-1234-5678",
            is_active=True,
            created_at=datetime.utcnow()
        )

        db_session.add(store)
        await db_session.commit()
        await db_session.refresh(store)

        assert store.code == "STORE-001"
        assert store.name == "강남1호점"
        assert store.is_active is True

    @pytest.mark.asyncio
    async def test_store_code_unique(self, db_session):
        """매장 코드는 유니크해야 함"""
        store1 = Store(
            id=uuid4(),
            code="STORE-001",
            name="매장1",
            created_at=datetime.utcnow()
        )

        store2 = Store(
            id=uuid4(),
            code="STORE-001",
            name="매장2",
            created_at=datetime.utcnow()
        )

        db_session.add(store1)
        await db_session.commit()

        db_session.add(store2)
        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()


class TestCategoryModel:
    """Category 모델 테스트"""

    @pytest.mark.asyncio
    async def test_create_category(self, db_session):
        """카테고리 생성 테스트"""
        category = Category(
            id=uuid4(),
            code="SK",
            name="스킨케어",
            sort_order=1,
            created_at=datetime.utcnow()
        )

        db_session.add(category)
        await db_session.commit()
        await db_session.refresh(category)

        assert category.code == "SK"
        assert category.name == "스킨케어"
        assert category.sort_order == 1


class TestProductModel:
    """Product 모델 테스트"""

    @pytest.mark.asyncio
    async def test_create_product(self, db_session):
        """제품 생성 테스트"""
        # Category 먼저 생성
        category = Category(
            id=uuid4(),
            code="SK",
            name="스킨케어",
            sort_order=1,
            created_at=datetime.utcnow()
        )
        db_session.add(category)
        await db_session.commit()

        # Product 생성
        product = Product(
            id=uuid4(),
            barcode="8801234567890",
            name="수분크림 50ml",
            category_id=category.id,
            safety_stock=10,
            is_active=True,
            created_at=datetime.utcnow()
        )

        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)

        assert product.barcode == "8801234567890"
        assert product.name == "수분크림 50ml"
        assert product.category_id == category.id
        assert product.safety_stock == 10

    @pytest.mark.asyncio
    async def test_product_barcode_unique(self, db_session):
        """바코드는 유니크해야 함"""
        category = Category(
            id=uuid4(),
            code="SK",
            name="스킨케어",
            sort_order=1,
            created_at=datetime.utcnow()
        )
        db_session.add(category)
        await db_session.commit()

        product1 = Product(
            id=uuid4(),
            barcode="8801234567890",
            name="제품1",
            category_id=category.id,
            created_at=datetime.utcnow()
        )

        product2 = Product(
            id=uuid4(),
            barcode="8801234567890",
            name="제품2",
            category_id=category.id,
            created_at=datetime.utcnow()
        )

        db_session.add(product1)
        await db_session.commit()

        db_session.add(product2)
        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_product_default_safety_stock(self, db_session):
        """안전재고 기본값은 10"""
        category = Category(
            id=uuid4(),
            code="SK",
            name="스킨케어",
            sort_order=1,
            created_at=datetime.utcnow()
        )
        db_session.add(category)
        await db_session.commit()

        product = Product(
            id=uuid4(),
            barcode="8801234567890",
            name="제품",
            category_id=category.id,
            created_at=datetime.utcnow()
        )

        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)

        assert product.safety_stock == 10


class TestInventoryTransactionModel:
    """InventoryTransaction 모델 테스트"""

    @pytest.mark.asyncio
    async def test_create_inbound_transaction(self, db_session):
        """입고 트랜잭션 생성 테스트"""
        # 필수 데이터 생성
        category = Category(id=uuid4(), code="SK", name="스킨케어", sort_order=1, created_at=datetime.utcnow())
        product = Product(id=uuid4(), barcode="8801234567890", name="제품", category_id=category.id, created_at=datetime.utcnow())
        store = Store(id=uuid4(), code="STORE-001", name="매장", created_at=datetime.utcnow())
        user = User(id=uuid4(), email="user@test.com", password_hash="hash", name="유저", created_at=datetime.utcnow())

        db_session.add_all([category, product, store, user])
        await db_session.commit()

        # 입고 트랜잭션
        transaction = InventoryTransaction(
            id=uuid4(),
            product_id=product.id,
            store_id=store.id,
            user_id=user.id,
            type=TransactionType.INBOUND,
            quantity=30,
            note="정기 입고",
            created_at=datetime.utcnow()
        )

        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        assert transaction.type == TransactionType.INBOUND
        assert transaction.quantity == 30
        assert transaction.synced_at is None  # 아직 동기화 안됨

    @pytest.mark.asyncio
    async def test_create_adjust_transaction_with_reason(self, db_session):
        """조정 트랜잭션은 사유 포함"""
        # 필수 데이터 생성
        category = Category(id=uuid4(), code="SK", name="스킨케어", sort_order=1, created_at=datetime.utcnow())
        product = Product(id=uuid4(), barcode="8801234567890", name="제품", category_id=category.id, created_at=datetime.utcnow())
        store = Store(id=uuid4(), code="STORE-001", name="매장", created_at=datetime.utcnow())
        user = User(id=uuid4(), email="user@test.com", password_hash="hash", name="유저", created_at=datetime.utcnow())

        db_session.add_all([category, product, store, user])
        await db_session.commit()

        # 조정 트랜잭션
        transaction = InventoryTransaction(
            id=uuid4(),
            product_id=product.id,
            store_id=store.id,
            user_id=user.id,
            type=TransactionType.ADJUST,
            quantity=-5,
            reason=AdjustReason.EXPIRED,
            note="유통기한 만료",
            created_at=datetime.utcnow()
        )

        db_session.add(transaction)
        await db_session.commit()
        await db_session.refresh(transaction)

        assert transaction.type == TransactionType.ADJUST
        assert transaction.reason == AdjustReason.EXPIRED
        assert transaction.quantity == -5


class TestCurrentStockModel:
    """CurrentStock 모델 테스트"""

    @pytest.mark.asyncio
    async def test_create_current_stock(self, db_session):
        """현재고 생성 테스트"""
        # 필수 데이터 생성
        category = Category(id=uuid4(), code="SK", name="스킨케어", sort_order=1, created_at=datetime.utcnow())
        product = Product(id=uuid4(), barcode="8801234567890", name="제품", category_id=category.id, created_at=datetime.utcnow())
        store = Store(id=uuid4(), code="STORE-001", name="매장", created_at=datetime.utcnow())

        db_session.add_all([category, product, store])
        await db_session.commit()

        # 현재고
        stock = CurrentStock(
            product_id=product.id,
            store_id=store.id,
            quantity=25,
            updated_at=datetime.utcnow()
        )

        db_session.add(stock)
        await db_session.commit()
        await db_session.refresh(stock)

        assert stock.product_id == product.id
        assert stock.store_id == store.id
        assert stock.quantity == 25

    @pytest.mark.asyncio
    async def test_current_stock_composite_key(self, db_session):
        """현재고는 (product_id, store_id) 복합키"""
        # 필수 데이터 생성
        category = Category(id=uuid4(), code="SK", name="스킨케어", sort_order=1, created_at=datetime.utcnow())
        product = Product(id=uuid4(), barcode="8801234567890", name="제품", category_id=category.id, created_at=datetime.utcnow())
        store = Store(id=uuid4(), code="STORE-001", name="매장", created_at=datetime.utcnow())

        db_session.add_all([category, product, store])
        await db_session.commit()

        stock1 = CurrentStock(
            product_id=product.id,
            store_id=store.id,
            quantity=25,
            updated_at=datetime.utcnow()
        )

        stock2 = CurrentStock(
            product_id=product.id,
            store_id=store.id,
            quantity=30,
            updated_at=datetime.utcnow()
        )

        db_session.add(stock1)
        await db_session.commit()

        db_session.add(stock2)
        with pytest.raises(Exception):  # IntegrityError (복합키 중복)
            await db_session.commit()
