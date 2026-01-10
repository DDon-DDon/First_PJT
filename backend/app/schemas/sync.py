from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.models.transaction import TransactionType, AdjustReason

class SyncTransactionItem(BaseModel):
    local_id: UUID = Field(..., alias="localId")
    type: TransactionType
    product_id: UUID = Field(..., alias="productId")
    store_id: UUID = Field(..., alias="storeId")
    quantity: int
    reason: Optional[AdjustReason] = None
    note: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")

    model_config = {"populate_by_name": True}

class SyncRequest(BaseModel):
    transactions: List[SyncTransactionItem]

class SyncedItem(BaseModel):
    local_id: UUID = Field(..., alias="localId")
    server_id: UUID = Field(..., alias="serverId")
    
    model_config = {"populate_by_name": True}

class FailedItem(BaseModel):
    local_id: UUID = Field(..., alias="localId")
    error: str
    
    model_config = {"populate_by_name": True}

class SyncResponse(BaseModel):
    synced: List[SyncedItem]
    failed: List[FailedItem]
    synced_at: datetime = Field(..., alias="syncedAt")
    
    model_config = {"populate_by_name": True}
