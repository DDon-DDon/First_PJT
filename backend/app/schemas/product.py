"""
Product 스키마 정의
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    """제품 생성 요청 스키마"""
    barcode: str = Field(..., min_length=1, max_length=50, description="바코드")
    name: str = Field(..., min_length=1, max_length=200, description="제품명")
    categoryId: str = Field(..., description="카테고리 ID")
    safetyStock: int = Field(default=10, ge=0, description="안전재고")
    imageUrl: Optional[str] = Field(None, max_length=500, description="이미지 URL")
    memo: Optional[str] = Field(None, description="메모")


class ProductResponse(BaseModel):
    """제품 응답 스키마"""
    id: UUID = Field(..., description="제품 ID")
    barcode: str = Field(..., description="바코드")
    name: str = Field(..., description="제품명")
    categoryId: UUID = Field(..., description="카테고리 ID")
    safetyStock: int = Field(..., description="안전재고")
    imageUrl: Optional[str] = Field(None, description="이미지 URL")
    memo: Optional[str] = Field(None, description="메모")
    isActive: bool = Field(..., description="활성 상태")
    createdAt: datetime = Field(..., description="생성 시각")
    updatedAt: Optional[datetime] = Field(None, description="수정 시각")

    model_config = {
        "from_attributes": True
    }
