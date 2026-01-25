from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.models.transaction import TransactionType, AdjustReason

class SyncTransactionItem(BaseModel):
    """동기화할 개별 트랜잭션 항목"""
    local_id: UUID = Field(..., alias="localId", description="클라이언트 로컬 ID")
    type: TransactionType = Field(..., description="트랜잭션 타입 (INBOUND, OUTBOUND, ADJUST)")
    product_id: UUID = Field(..., alias="productId", description="제품 ID")
    store_id: UUID = Field(..., alias="storeId", description="매장 ID")
    quantity: int = Field(..., description="수량 (양수=입고, 음수=출고/조정)")
    reason: Optional[AdjustReason] = Field(None, description="조정 사유 (ADJUST일 때만)")
    note: Optional[str] = Field(None, description="비고")
    created_at: datetime = Field(..., alias="createdAt", description="클라이언트에서 생성된 시각")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "localId": "110e8400-e29b-41d4-a716-446655440000",
                "type": "INBOUND",
                "productId": "550e8400-e29b-41d4-a716-446655440000",
                "storeId": "660e8400-e29b-41d4-a716-446655440000",
                "quantity": 20,
                "reason": None,
                "note": "오프라인 입고",
                "createdAt": "2026-01-24T08:30:00Z"
            }
        }
    }

class SyncRequest(BaseModel):
    """오프라인 동기화 요청 스키마"""
    transactions: List[SyncTransactionItem] = Field(..., description="동기화할 트랜잭션 목록")

    model_config = {
        "json_schema_extra": {
            "example": {
                "transactions": [
                    {
                        "localId": "110e8400-e29b-41d4-a716-446655440000",
                        "type": "INBOUND",
                        "productId": "550e8400-e29b-41d4-a716-446655440000",
                        "storeId": "660e8400-e29b-41d4-a716-446655440000",
                        "quantity": 20,
                        "reason": None,
                        "note": "오프라인 입고",
                        "createdAt": "2026-01-24T08:30:00Z"
                    },
                    {
                        "localId": "220e8400-e29b-41d4-a716-446655440000",
                        "type": "OUTBOUND",
                        "productId": "550e8400-e29b-41d4-a716-446655440000",
                        "storeId": "660e8400-e29b-41d4-a716-446655440000",
                        "quantity": 5,
                        "reason": None,
                        "note": "오프라인 판매",
                        "createdAt": "2026-01-24T09:00:00Z"
                    }
                ]
            }
        }
    }


class SyncedItem(BaseModel):
    """동기화 성공 항목"""
    local_id: UUID = Field(..., alias="localId", description="클라이언트 로컬 ID")
    server_id: UUID = Field(..., alias="serverId", description="서버에서 생성된 트랜잭션 ID")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "localId": "110e8400-e29b-41d4-a716-446655440000",
                "serverId": "880e8400-e29b-41d4-a716-446655440000"
            }
        }
    }


class FailedItem(BaseModel):
    """동기화 실패 항목"""
    local_id: UUID = Field(..., alias="localId", description="클라이언트 로컬 ID")
    error: str = Field(..., description="실패 사유")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "localId": "220e8400-e29b-41d4-a716-446655440000",
                "error": "재고 부족: 현재 5개, 요청 10개"
            }
        }
    }


class SyncResponse(BaseModel):
    """동기화 응답 스키마"""
    synced: List[SyncedItem] = Field(..., description="성공한 항목 목록")
    failed: List[FailedItem] = Field(..., description="실패한 항목 목록")
    synced_at: datetime = Field(..., alias="syncedAt", description="동기화 완료 시각")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "synced": [
                    {
                        "localId": "110e8400-e29b-41d4-a716-446655440000",
                        "serverId": "880e8400-e29b-41d4-a716-446655440000"
                    }
                ],
                "failed": [
                    {
                        "localId": "220e8400-e29b-41d4-a716-446655440000",
                        "error": "재고 부족: 현재 5개, 요청 10개"
                    }
                ],
                "syncedAt": "2026-01-24T10:00:00Z"
            }
        }
    }
