"""
User 스키마 정의
"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """사용자 생성 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    name: str = Field(..., min_length=1, max_length=100, description="이름")
    role: str = Field(default="WORKER", description="역할")


class UserResponse(BaseModel):
    """사용자 응답 스키마"""
    id: UUID = Field(..., description="사용자 ID")
    email: EmailStr = Field(..., description="이메일")
    name: str = Field(..., description="이름")
    role: str = Field(..., description="역할")
    isActive: bool = Field(..., description="활성 상태")
    createdAt: datetime = Field(..., description="생성 시각")
    updatedAt: Optional[datetime] = Field(None, description="수정 시각")

    model_config = {
        "from_attributes": True
    }
