from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.user import User
from app.models.transaction import InventoryTransaction, TransactionType
from app.schemas.sync import SyncRequest, SyncResponse, SyncedItem, FailedItem
from app.services import inventory as inventory_service
from app.schemas.transaction import (
    InboundTransactionCreate, OutboundTransactionCreate, AdjustTransactionCreate
)

async def sync_transactions(
    db: AsyncSession, 
    request: SyncRequest, 
    user: Optional[User] = None  # TODO: 인증 구현 후 필수로 변경
) -> SyncResponse:
    
    synced_items = []
    failed_items = []
    
    for tx_item in request.transactions:
        # 1. 중복 체크 (local_id)
        stmt = select(InventoryTransaction).where(InventoryTransaction.local_id == tx_item.local_id)
        result = await db.execute(stmt)
        existing_tx = result.scalar_one_or_none()
        
        if existing_tx:
            synced_items.append(SyncedItem(localId=tx_item.local_id, serverId=existing_tx.id))
            continue
            
        # 2. 트랜잭션 처리
        try:
            tx = None
            if tx_item.type == TransactionType.INBOUND:
                data = InboundTransactionCreate(
                    product_id=str(tx_item.product_id),
                    store_id=str(tx_item.store_id),
                    quantity=tx_item.quantity,
                    note=tx_item.note
                )
                tx, _, _ = await inventory_service.process_inbound(db, data, user)
                
            elif tx_item.type == TransactionType.OUTBOUND:
                data = OutboundTransactionCreate(
                    product_id=str(tx_item.product_id),
                    store_id=str(tx_item.store_id),
                    quantity=tx_item.quantity,
                    note=tx_item.note
                )
                tx, _, _ = await inventory_service.process_outbound(db, data, user)
                
            elif tx_item.type == TransactionType.ADJUST:
                if not tx_item.reason:
                    raise ValueError("Reason is required for ADJUST")
                    
                data = AdjustTransactionCreate(
                    product_id=str(tx_item.product_id),
                    store_id=str(tx_item.store_id),
                    quantity=tx_item.quantity,
                    reason=tx_item.reason,
                    note=tx_item.note
                )
                tx, _, _ = await inventory_service.process_adjust(db, data, user)
            
            # 3. 추가 메타데이터 업데이트
            if tx:
                tx.local_id = tx_item.local_id
                tx.created_at = tx_item.created_at
                tx.synced_at = datetime.utcnow()
                
                db.add(tx)
                await db.commit()
                
                synced_items.append(SyncedItem(localId=tx_item.local_id, serverId=tx.id))
            else:
                raise ValueError("Unknown transaction type")
            
        except Exception as e:
            # 트랜잭션 처리 중 오류 발생 시 롤백
            await db.rollback()
            failed_items.append(FailedItem(localId=tx_item.local_id, error=str(e)))
            
    return SyncResponse(
        synced=synced_items,
        failed=failed_items,
        syncedAt=datetime.utcnow()
    )
