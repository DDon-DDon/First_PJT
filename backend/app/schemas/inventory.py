from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import Pagination
from app.schemas.product import ProductResponse

class ProductSimpleResponse(BaseModel):
    id: UUID
    barcode: str
    name: str
    safety_stock: int = Field(..., alias="safetyStock")
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class StoreSimpleResponse(BaseModel):
    id: UUID
    name: str
    code: str

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class StockItemResponse(BaseModel):
    product: ProductSimpleResponse
    store: StoreSimpleResponse
    quantity: int
    status: str
    last_alerted_at: Optional[datetime] = Field(None, alias="lastAlertedAt")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class StockListResponse(BaseModel):
    items: List[StockItemResponse]
    pagination: Pagination

class ProductStockDetailResponse(BaseModel):
    product: ProductResponse
    stocks: List[StockItemResponse]
    total_quantity: int = Field(..., alias="totalQuantity")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
