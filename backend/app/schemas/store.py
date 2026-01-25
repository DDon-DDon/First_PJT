from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class StoreBase(BaseModel):
    code: str = Field(..., description="매장 코드 (예: GN001)")
    name: str = Field(..., description="매장명")
    address: Optional[str] = Field(None, description="매장 주소")
    phone: Optional[str] = Field(None, description="매장 연락처")
    is_active: bool = Field(default=True, alias="isActive", description="활성화 여부")

    model_config = {
        "populate_by_name": True
    }


class StoreCreate(StoreBase):
    """매장 생성 요청 스키마"""

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "code": "GN001",
                "name": "강남점",
                "address": "서울시 강남구 테헤란로 123",
                "phone": "02-1234-5678",
                "isActive": True
            }
        }
    }


class StoreUpdate(BaseModel):
    """매장 수정 요청 스키마"""
    name: Optional[str] = Field(None, description="매장명")
    address: Optional[str] = Field(None, description="매장 주소")
    phone: Optional[str] = Field(None, description="매장 연락처")
    is_active: Optional[bool] = Field(None, alias="isActive", description="활성화 여부")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "강남점 (리뉴얼)",
                "address": "서울시 강남구 테헤란로 456",
                "phone": "02-9876-5432",
                "isActive": True
            }
        }
    }


class StoreResponse(StoreBase):
    """매장 응답 스키마"""
    id: UUID = Field(..., description="매장 고유 식별자")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "code": "GN001",
                "name": "강남점",
                "address": "서울시 강남구 테헤란로 123",
                "phone": "02-1234-5678",
                "isActive": True
            }
        }
    }
