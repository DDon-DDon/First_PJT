"""
재고 서비스 단위 테스트

서비스 레이어의 비즈니스 로직을 단위 테스트합니다.
DB 의존성은 Mock으로 대체합니다.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from app.services.inventory import (
    get_stock_status,
    process_inbound,
    process_outbound,
    process_adjust,
)
from app.core.exceptions import InsufficientStockException
from app.models.user import User, UserRole
from app.models.stock import CurrentStock
from app.models.product import Product
from app.models.transaction import TransactionType


class TestGetStockStatus:
    """재고 상태 계산 테스트"""

    @pytest.mark.parametrize("quantity,safety_stock,expected", [
        (0, 10, "LOW"),      # 0 < 10: LOW
        (5, 10, "LOW"),      # 5 < 10: LOW
        (9, 10, "LOW"),      # 9 < 10: LOW
        (10, 10, "NORMAL"),  # 10 >= 10 and 10 < 20: NORMAL
        (15, 10, "NORMAL"),  # 15 >= 10 and 15 < 20: NORMAL
        (19, 10, "NORMAL"),  # 19 >= 10 and 19 < 20: NORMAL
        (20, 10, "GOOD"),    # 20 >= 20: GOOD
        (100, 10, "GOOD"),   # 100 >= 20: GOOD
    ])
    def test_stock_status_calculation(self, quantity, safety_stock, expected):
        """재고량과 안전재고에 따른 상태 계산"""
        assert get_stock_status(quantity, safety_stock) == expected

    def test_zero_safety_stock(self):
        """안전재고가 0일 때"""
        # safety_stock=0이면 quantity >= 0 이므로 GOOD
        assert get_stock_status(0, 0) == "GOOD"
        assert get_stock_status(1, 0) == "GOOD"


class TestProcessInbound:
    """입고 처리 테스트"""

    @pytest.fixture
    def mock_db(self):
        """Mock DB 세션"""
        db = AsyncMock()
        return db

    @pytest.fixture
    def mock_user(self):
        """Mock 사용자"""
        user = MagicMock(spec=User)
        user.id = uuid4()
        user.role = UserRole.WORKER
        return user

    @pytest.fixture
    def mock_product(self):
        """Mock 제품"""
        product = MagicMock(spec=Product)
        product.id = uuid4()
        product.safety_stock = 10
        return product

    @pytest.fixture
    def mock_stock(self, mock_product):
        """Mock 재고"""
        stock = MagicMock(spec=CurrentStock)
        stock.product_id = mock_product.id
        stock.store_id = uuid4()
        stock.quantity = 10
        stock.product = mock_product
        return stock

    @pytest.mark.asyncio
    async def test_inbound_increases_stock(self, mock_db, mock_user, mock_stock):
        """입고 시 재고 증가"""
        from app.schemas.transaction import InboundTransactionCreate

        # Given
        initial_quantity = mock_stock.quantity
        inbound_qty = 20

        data = InboundTransactionCreate(
            productId=str(mock_stock.product_id),
            storeId=str(mock_stock.store_id),
            quantity=inbound_qty,
            note="테스트 입고"
        )

        # Mock _get_or_create_stock
        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = mock_stock

            # When
            tx, new_qty, alert = await process_inbound(mock_db, data, mock_user)

            # Then
            assert mock_stock.quantity == initial_quantity + inbound_qty
            assert new_qty == initial_quantity + inbound_qty
            assert alert is False
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()


class TestProcessOutbound:
    """출고 처리 테스트"""

    @pytest.fixture
    def mock_db(self):
        """Mock DB 세션"""
        db = AsyncMock()
        return db

    @pytest.fixture
    def mock_user(self):
        """Mock 사용자"""
        user = MagicMock(spec=User)
        user.id = uuid4()
        user.role = UserRole.WORKER
        return user

    @pytest.fixture
    def mock_product(self):
        """Mock 제품"""
        product = MagicMock(spec=Product)
        product.id = uuid4()
        product.safety_stock = 10
        return product

    @pytest.fixture
    def mock_stock(self, mock_product):
        """Mock 재고 (충분한 재고)"""
        stock = MagicMock(spec=CurrentStock)
        stock.product_id = mock_product.id
        stock.store_id = uuid4()
        stock.quantity = 50
        stock.product = mock_product
        return stock

    @pytest.mark.asyncio
    async def test_outbound_decreases_stock(self, mock_db, mock_user, mock_stock):
        """출고 시 재고 감소"""
        from app.schemas.transaction import OutboundTransactionCreate

        # Given
        initial_quantity = mock_stock.quantity
        outbound_qty = 10

        data = OutboundTransactionCreate(
            productId=str(mock_stock.product_id),
            storeId=str(mock_stock.store_id),
            quantity=outbound_qty,
            note="테스트 출고"
        )

        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = mock_stock

            # When
            tx, new_qty, alert = await process_outbound(mock_db, data, mock_user)

            # Then
            assert mock_stock.quantity == initial_quantity - outbound_qty
            assert new_qty == initial_quantity - outbound_qty
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_outbound_insufficient_stock_raises_error(self, mock_db, mock_user, mock_product):
        """재고 부족 시 예외 발생"""
        from app.schemas.transaction import OutboundTransactionCreate

        # Given - 재고가 5개뿐인 상황
        stock = MagicMock(spec=CurrentStock)
        stock.product_id = mock_product.id
        stock.store_id = uuid4()
        stock.quantity = 5
        stock.product = mock_product

        data = OutboundTransactionCreate(
            productId=str(stock.product_id),
            storeId=str(stock.store_id),
            quantity=10,  # 5개밖에 없는데 10개 출고 시도
            note="재고 부족 테스트"
        )

        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = stock

            # When & Then
            with pytest.raises(InsufficientStockException):
                await process_outbound(mock_db, data, mock_user)

            # 커밋이 호출되지 않아야 함
            mock_db.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_outbound_triggers_safety_alert(self, mock_db, mock_user, mock_product):
        """출고 후 안전재고 미만이면 알림 발생"""
        from app.schemas.transaction import OutboundTransactionCreate

        # Given - 재고 15개, 안전재고 10개, 10개 출고 → 5개 남음 (LOW)
        stock = MagicMock(spec=CurrentStock)
        stock.product_id = mock_product.id
        stock.store_id = uuid4()
        stock.quantity = 15
        stock.product = mock_product
        mock_product.safety_stock = 10

        data = OutboundTransactionCreate(
            productId=str(stock.product_id),
            storeId=str(stock.store_id),
            quantity=10,
            note="안전재고 알림 테스트"
        )

        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = stock

            # When
            tx, new_qty, alert = await process_outbound(mock_db, data, mock_user)

            # Then
            assert new_qty == 5
            assert alert is True  # 5 < 10 → 안전재고 미만


class TestProcessAdjust:
    """재고 조정 테스트"""

    @pytest.fixture
    def mock_db(self):
        """Mock DB 세션"""
        db = AsyncMock()
        return db

    @pytest.fixture
    def mock_user(self):
        """Mock 사용자"""
        user = MagicMock(spec=User)
        user.id = uuid4()
        user.role = UserRole.ADMIN
        return user

    @pytest.fixture
    def mock_product(self):
        """Mock 제품"""
        product = MagicMock(spec=Product)
        product.id = uuid4()
        product.safety_stock = 10
        return product

    @pytest.fixture
    def mock_stock(self, mock_product):
        """Mock 재고"""
        stock = MagicMock(spec=CurrentStock)
        stock.product_id = mock_product.id
        stock.store_id = uuid4()
        stock.quantity = 20
        stock.product = mock_product
        return stock

    @pytest.mark.asyncio
    async def test_adjust_positive_increases_stock(self, mock_db, mock_user, mock_stock):
        """양수 조정 시 재고 증가 (반품 등)"""
        from app.schemas.transaction import AdjustTransactionCreate
        from app.models.transaction import AdjustReason

        initial_quantity = mock_stock.quantity
        adjust_qty = 5

        data = AdjustTransactionCreate(
            productId=str(mock_stock.product_id),
            storeId=str(mock_stock.store_id),
            quantity=adjust_qty,
            reason=AdjustReason.CORRECTION,
            note="재고 정정 (반품)"
        )

        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = mock_stock

            tx, new_qty, alert = await process_adjust(mock_db, data, mock_user)

            assert mock_stock.quantity == initial_quantity + adjust_qty
            assert new_qty == initial_quantity + adjust_qty

    @pytest.mark.asyncio
    async def test_adjust_negative_decreases_stock(self, mock_db, mock_user, mock_stock):
        """음수 조정 시 재고 감소 (분실/파손 등)"""
        from app.schemas.transaction import AdjustTransactionCreate
        from app.models.transaction import AdjustReason

        initial_quantity = mock_stock.quantity
        adjust_qty = -5

        data = AdjustTransactionCreate(
            productId=str(mock_stock.product_id),
            storeId=str(mock_stock.store_id),
            quantity=adjust_qty,
            reason=AdjustReason.DAMAGED,
            note="파손 폐기"
        )

        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = mock_stock

            tx, new_qty, alert = await process_adjust(mock_db, data, mock_user)

            assert mock_stock.quantity == initial_quantity + adjust_qty
            assert new_qty == initial_quantity + adjust_qty

    @pytest.mark.asyncio
    async def test_adjust_cannot_go_below_zero(self, mock_db, mock_user, mock_product):
        """조정으로 재고가 0 미만이 될 수 없음"""
        from app.schemas.transaction import AdjustTransactionCreate
        from app.models.transaction import AdjustReason

        # Given - 재고 5개인데 10개 감소 시도
        stock = MagicMock(spec=CurrentStock)
        stock.product_id = mock_product.id
        stock.store_id = uuid4()
        stock.quantity = 5
        stock.product = mock_product

        data = AdjustTransactionCreate(
            productId=str(stock.product_id),
            storeId=str(stock.store_id),
            quantity=-10,
            reason=AdjustReason.OTHER,
            note="분실 처리"
        )

        with patch(
            'app.services.inventory._get_or_create_stock',
            new_callable=AsyncMock
        ) as mock_get_stock:
            mock_get_stock.return_value = stock

            with pytest.raises(InsufficientStockException):
                await process_adjust(mock_db, data, mock_user)
