from pydantic import BaseModel, Field
from app.schemas.product import ProductResponse
from app.schemas.store import StoreResponse

class LowStockItemResponse(BaseModel):
    """안전재고 부족 항목 응답 스키마"""
    product: ProductResponse
    store: StoreResponse
    current_stock: int = Field(..., alias="currentStock", description="현재 재고 수량")
    shortage: int = Field(..., description="부족 수량 (안전재고 - 현재재고)")

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
                "store": {
                    "id": "660e8400-e29b-41d4-a716-446655440000",
                    "name": "강남점",
                    "code": "GN001",
                    "address": "서울시 강남구",
                    "isActive": True,
                    "createdAt": "2026-01-01T09:00:00Z"
                },
                "currentStock": 3,
                "shortage": 7
            }
        }
    }
