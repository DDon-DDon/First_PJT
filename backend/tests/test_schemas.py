"""
🔴 RED: Pydantic 스키마 검증 테스트
"""
import pytest
from datetime import datetime
from uuid import uuid4
from pydantic import ValidationError


# ========== User 스키마 테스트 ==========

class TestUserSchemas:
    """User 스키마 테스트"""

    def test_user_create_schema_valid(self):
        """UserCreate 스키마 - 정상 데이터"""
        from app.schemas.user import UserCreate

        data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "테스트유저",
            "role": "WORKER"
        }
        user_create = UserCreate(**data)

        assert user_create.email == "test@example.com"
        assert user_create.password == "password123"
        assert user_create.name == "테스트유저"
        assert user_create.role == "WORKER"

    def test_user_create_schema_default_role(self):
        """UserCreate 스키마 - 기본 역할은 WORKER"""
        from app.schemas.user import UserCreate

        data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "테스트유저"
        }
        user_create = UserCreate(**data)

        assert user_create.role == "WORKER"

    def test_user_create_schema_invalid_email(self):
        """UserCreate 스키마 - 잘못된 이메일"""
        from app.schemas.user import UserCreate

        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                password="password123",
                name="테스트"
            )

    def test_user_response_schema(self):
        """UserResponse 스키마 - 응답 데이터"""
        from app.schemas.user import UserResponse

        data = {
            "id": uuid4(),
            "email": "test@example.com",
            "name": "테스트유저",
            "role": "WORKER",
            "isActive": True,
            "createdAt": datetime.utcnow()
        }
        user_response = UserResponse(**data)

        assert user_response.email == "test@example.com"
        assert user_response.role == "WORKER"
        assert user_response.isActive is True
        assert "password" not in user_response.model_dump()


# ========== Product 스키마 테스트 ==========

class TestProductSchemas:
    """Product 스키마 테스트"""

    def test_product_create_schema_valid(self):
        """ProductCreate 스키마 - 정상 데이터"""
        from app.schemas.product import ProductCreate

        data = {
            "barcode": "8801234567890",
            "name": "테스트제품",
            "categoryId": str(uuid4()),
            "safetyStock": 10
        }
        product_create = ProductCreate(**data)

        assert product_create.barcode == "8801234567890"
        assert product_create.name == "테스트제품"
        assert product_create.safetyStock == 10

    def test_product_create_schema_default_safety_stock(self):
        """ProductCreate 스키마 - 안전재고 기본값 10"""
        from app.schemas.product import ProductCreate

        data = {
            "barcode": "8801234567890",
            "name": "테스트제품",
            "categoryId": str(uuid4())
        }
        product_create = ProductCreate(**data)

        assert product_create.safetyStock == 10

    def test_product_response_schema(self):
        """ProductResponse 스키마 - 응답 데이터"""
        from app.schemas.product import ProductResponse

        data = {
            "id": uuid4(),
            "barcode": "8801234567890",
            "name": "테스트제품",
            "categoryId": uuid4(),
            "safetyStock": 10,
            "isActive": True,
            "createdAt": datetime.utcnow()
        }
        product_response = ProductResponse(**data)

        assert product_response.barcode == "8801234567890"
        assert product_response.isActive is True


# ========== Transaction 스키마 테스트 ==========

class TestTransactionSchemas:
    """Transaction 스키마 테스트"""

    def test_inbound_transaction_create_schema(self):
        """입고 트랜잭션 생성 스키마"""
        from app.schemas.transaction import InboundTransactionCreate

        data = {
            "productId": str(uuid4()),
            "storeId": str(uuid4()),
            "quantity": 30,
            "note": "정기 입고"
        }
        txn = InboundTransactionCreate(**data)

        assert txn.quantity == 30
        assert txn.note == "정기 입고"

    def test_outbound_transaction_create_schema(self):
        """출고 트랜잭션 생성 스키마"""
        from app.schemas.transaction import OutboundTransactionCreate

        data = {
            "productId": str(uuid4()),
            "storeId": str(uuid4()),
            "quantity": 10
        }
        txn = OutboundTransactionCreate(**data)

        assert txn.quantity == 10

    def test_adjust_transaction_create_schema(self):
        """조정 트랜잭션 생성 스키마"""
        from app.schemas.transaction import AdjustTransactionCreate

        data = {
            "productId": str(uuid4()),
            "storeId": str(uuid4()),
            "quantity": -5,
            "reason": "EXPIRED",
            "note": "유통기한 만료"
        }
        txn = AdjustTransactionCreate(**data)

        assert txn.quantity == -5
        assert txn.reason == "EXPIRED"

    def test_transaction_response_schema(self):
        """트랜잭션 응답 스키마"""
        from app.schemas.transaction import TransactionResponse

        data = {
            "id": uuid4(),
            "productId": uuid4(),
            "storeId": uuid4(),
            "userId": uuid4(),
            "type": "INBOUND",
            "quantity": 30,
            "createdAt": datetime.utcnow()
        }
        txn_response = TransactionResponse(**data)

        assert txn_response.type == "INBOUND"
        assert txn_response.quantity == 30


# ========== Common 스키마 테스트 ==========

class TestCommonSchemas:
    """Common 스키마 테스트"""

    def test_pagination_schema(self):
        """Pagination 스키마"""
        from app.schemas.common import Pagination

        data = {
            "page": 1,
            "limit": 20,
            "total": 100,
            "totalPages": 5
        }
        pagination = Pagination(**data)

        assert pagination.page == 1
        assert pagination.limit == 20
        assert pagination.total == 100
        assert pagination.totalPages == 5

    def test_error_response_schema(self):
        """ErrorResponse 스키마"""
        from app.schemas.common import ErrorResponse

        data = {
            "code": "PRODUCT_NOT_FOUND",
            "message": "제품을 찾을 수 없습니다",
            "details": {"barcode": "8801234567890"}
        }
        error = ErrorResponse(**data)

        assert error.code == "PRODUCT_NOT_FOUND"
        assert error.message == "제품을 찾을 수 없습니다"
        assert error.details["barcode"] == "8801234567890"

    def test_success_response_schema(self):
        """SuccessResponse 스키마"""
        from app.schemas.common import SuccessResponse

        data = {
            "success": True,
            "data": {"id": str(uuid4()), "name": "테스트"}
        }
        response = SuccessResponse(**data)

        assert response.success is True
        assert "id" in response.data
