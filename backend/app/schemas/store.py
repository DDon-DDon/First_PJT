from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class StoreResponse(BaseModel):
    id: UUID
    code: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = Field(..., alias="isActive")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
