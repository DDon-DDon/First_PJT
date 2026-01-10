from pydantic import BaseModel, Field
from uuid import UUID

class CategoryResponse(BaseModel):
    id: UUID
    code: str
    name: str
    sort_order: int = Field(..., alias="sortOrder")

    model_config = {
        "from_attributes": True, 
        "populate_by_name": True
    }
