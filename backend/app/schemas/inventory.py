from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import Pagination
from app.schemas.product import ProductResponse

class ProductSimpleResponse(BaseModel):
    """제품 간략 정보 (재고 조회 시 사용)"""
    id: UUID = Field(..., description="제품 고유 식별자")
    barcode: str = Field(..., description="제품 바코드")
    name: str = Field(..., description="제품명")
    safety_stock: int = Field(..., alias="safetyStock", description="설정된 안전재고 수량")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "barcode": "8801234567890",
                "name": "새우깡",
                "safetyStock": 10
            }
        }
    }

class StoreSimpleResponse(BaseModel):
    """매장 간략 정보 (재고 조회 시 사용)"""
    id: UUID = Field(..., description="매장 고유 식별자")
    name: str = Field(..., description="매장명")
    code: str = Field(..., description="매장 코드")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "name": "강남점",
                "code": "GN001"
            }
        }
    }

class StockItemResponse(BaseModel):
    """재고 항목 응답 스키마"""
    product: ProductSimpleResponse
    store: StoreSimpleResponse
    quantity: int = Field(..., description="현재 재고 수량")
    status: str = Field(..., description="재고 상태 (NORMAL, LOW, OUT)")
    last_alerted_at: Optional[datetime] = Field(None, alias="lastAlertedAt", description="마지막 안전재고 알림 일시")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "product": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "barcode": "8801234567890",
                    "name": "새우깡",
                    "safetyStock": 10
                },
                "store": {
                    "id": "660e8400-e29b-41d4-a716-446655440000",
                    "name": "강남점",
                    "code": "GN001"
                },
                "quantity": 25,
                "status": "NORMAL",
                "lastAlertedAt": None
            }
        }
    }

class StockListResponse(BaseModel):
    """재고 목록 응답 스키마"""
    items: List[StockItemResponse]
    pagination: Pagination

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {
                        "product": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "barcode": "8801234567890",
                            "name": "새우깡",
                            "safetyStock": 10
                        },
                        "store": {
                            "id": "660e8400-e29b-41d4-a716-446655440000",
                            "name": "강남점",
                            "code": "GN001"
                        },
                        "quantity": 25,
                        "status": "NORMAL",
                        "lastAlertedAt": None
                    }
                ],
                "pagination": {
                    "page": 1,
                    "limit": 10,
                    "total": 1,
                    "totalPages": 1
                }
            }
        }
    }


class ProductStockDetailResponse(BaseModel):
    """제품별 재고 상세 응답 스키마"""
    product: ProductResponse
    stocks: List[StockItemResponse] = Field(..., description="매장별 재고 목록")
    total_quantity: int = Field(..., alias="totalQuantity", description="전체 매장 합계 재고")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "product": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "barcode": "8801234567890",
                    "name": "새우깡",
                    "categoryId": "770e8400-e29b-41d4-a716-446655440000",
                    "safetyStock": 10,
                    "imageUrl": None,
                    "memo": None,
                    "isActive": True,
                    "createdAt": "2026-01-01T09:00:00Z",
                    "updatedAt": None
                },
                "stocks": [
                    {
                        "product": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "barcode": "8801234567890",
                            "name": "새우깡",
                            "safetyStock": 10
                        },
                        "store": {
                            "id": "660e8400-e29b-41d4-a716-446655440000",
                            "name": "강남점",
                            "code": "GN001"
                        },
                        "quantity": 25,
                        "status": "NORMAL",
                        "lastAlertedAt": None
                    }
                ],
                "totalQuantity": 25
            }
        }
    }
