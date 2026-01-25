from pydantic import BaseModel, Field
from uuid import UUID

class CategoryCreate(BaseModel):
    code: str
    name: str
    sort_order: int = Field(..., alias="sortOrder")

    model_config = {
        "populate_by_name": True
    }

class CategoryResponse(BaseModel):
    """카테고리 응답 스키마"""
    id: UUID = Field(..., description="카테고리 고유 식별자")
    code: str = Field(..., description="카테고리 코드 (예: SNACK)")
    name: str = Field(..., description="카테고리명")
    sort_order: int = Field(..., alias="sortOrder", description="정렬 순서 (낮을수록 먼저)")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "770e8400-e29b-41d4-a716-446655440000",
                "code": "SNACK",
                "name": "스낵",
                "sortOrder": 1
            }
        }
    }
