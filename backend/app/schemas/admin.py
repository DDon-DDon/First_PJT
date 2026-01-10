from pydantic import BaseModel, Field
from app.schemas.product import ProductResponse
from app.schemas.store import StoreResponse

class LowStockItemResponse(BaseModel):
    product: ProductResponse
    store: StoreResponse
    current_stock: int = Field(..., alias="currentStock")
    shortage: int

    model_config = {
        "from_attributes": True, 
        "populate_by_name": True
    }
