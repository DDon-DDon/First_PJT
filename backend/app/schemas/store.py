from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class StoreBase(BaseModel):
    code: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = Field(default=True, alias="isActive")

class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = Field(None, alias="isActive")

class StoreResponse(StoreBase):
    id: UUID

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
