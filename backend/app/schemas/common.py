"""
공통 스키마 정의
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict


class Pagination(BaseModel):
    """페이지네이션 정보"""
    page: int = Field(..., ge=1, description="현재 페이지")
    limit: int = Field(..., ge=1, le=100, description="페이지당 항목 수")
    total: int = Field(..., ge=0, description="전체 항목 수")
    totalPages: int = Field(..., ge=0, description="전체 페이지 수")


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    code: str = Field(..., description="에러 코드")
    message: str = Field(..., description="에러 메시지")
    details: Optional[Dict[str, Any]] = Field(None, description="상세 정보")


class SuccessResponse(BaseModel):
    """성공 응답 스키마"""
    success: bool = Field(True, description="성공 여부")
    data: Any = Field(..., description="응답 데이터")
