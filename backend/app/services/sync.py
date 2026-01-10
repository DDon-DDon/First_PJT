from typing import List
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
    user: User
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
                    productId=str(tx_item.product_id),
                    storeId=str(tx_item.store_id),
                    quantity=tx_item.quantity,
                    note=tx_item.note
                )
                tx, _, _ = await inventory_service.process_inbound(db, data, user)
                
            elif tx_item.type == TransactionType.OUTBOUND:
                data = OutboundTransactionCreate(
                    productId=str(tx_item.product_id),
                    storeId=str(tx_item.store_id),
                    quantity=tx_item.quantity,
                    note=tx_item.note
                )
                tx, _, _ = await inventory_service.process_outbound(db, data, user)
                
            elif tx_item.type == TransactionType.ADJUST:
                if not tx_item.reason:
                    raise ValueError("Reason is required for ADJUST")
                    
                data = AdjustTransactionCreate(
                    productId=str(tx_item.product_id),
                    storeId=str(tx_item.store_id),
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
            # 트랜잭션 처리 중 오류 발생 시 롤백은 process_... 내부에서 발생하지 않음 (process_...는 성공 시 commit함)
            # 하지만 process_... 가 에러를 raise하면 DB는 clean state (rollback in deps or session manager)
            # 여기서는 loop 내에서 개별 처리하므로, process_... 실패 시 rollback이 필요할 수 있음.
            # 하지만 process_... 함수는 에러 발생 시 commit하지 않음.
            # 안전을 위해 explicit rollback for current session state if needed?
            # FastAPI dependency session automatically rolls back on exception?
            # But we are catching exception here.
            # So we must rollback manually to clear the failed transaction state if any.
            await db.rollback()
            failed_items.append(FailedItem(localId=tx_item.local_id, error=str(e)))
            
    return SyncResponse(
        synced=synced_items,
        failed=failed_items,
        syncedAt=datetime.utcnow()
    )
