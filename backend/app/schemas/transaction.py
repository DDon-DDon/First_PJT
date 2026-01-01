"""
Transaction 스키마 정의
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class InboundTransactionCreate(BaseModel):
    """입고 트랜잭션 생성 요청"""
    productId: str = Field(..., description="제품 ID")
    storeId: str = Field(..., description="매장 ID")
    quantity: int = Field(..., gt=0, description="입고 수량")
    note: Optional[str] = Field(None, description="비고")


class OutboundTransactionCreate(BaseModel):
    """출고 트랜잭션 생성 요청"""
    productId: str = Field(..., description="제품 ID")
    storeId: str = Field(..., description="매장 ID")
    quantity: int = Field(..., gt=0, description="출고 수량")
    note: Optional[str] = Field(None, description="비고")


class AdjustTransactionCreate(BaseModel):
    """조정 트랜잭션 생성 요청"""
    productId: str = Field(..., description="제품 ID")
    storeId: str = Field(..., description="매장 ID")
    quantity: int = Field(..., description="조정 수량")
    reason: str = Field(..., description="조정 사유")
    note: Optional[str] = Field(None, description="비고")


class TransactionResponse(BaseModel):
    """트랜잭션 응답 스키마"""
    id: UUID = Field(..., description="트랜잭션 ID")
    productId: UUID = Field(..., description="제품 ID")
    storeId: UUID = Field(..., description="매장 ID")
    userId: UUID = Field(..., description="작업자 ID")
    type: str = Field(..., description="트랜잭션 타입")
    quantity: int = Field(..., description="수량")
    reason: Optional[str] = Field(None, description="조정 사유")
    note: Optional[str] = Field(None, description="비고")
    createdAt: datetime = Field(..., description="생성 시각")
    syncedAt: Optional[datetime] = Field(None, description="동기화 시각")

    model_config = {
        "from_attributes": True
    }
