from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
# TODO: 인증 구현 후 활성화 (나중에 구현 예정)
# from app.api.deps import get_current_user
# from app.models.user import User
from app.schemas.transaction import (
    InboundTransactionCreate,
    OutboundTransactionCreate,
    AdjustTransactionCreate,
    TransactionResultResponse,
    TransactionListResponse
)
from app.services import inventory as inventory_service

router = APIRouter()

@router.post("/inbound", response_model=TransactionResultResponse, status_code=status.HTTP_201_CREATED)
async def inbound(
    data: InboundTransactionCreate,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """입고 처리"""
    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    tx, new_stock, _ = await inventory_service.process_inbound(db, data, user=None)
    
    resp = TransactionResultResponse.model_validate(tx)
    resp.new_stock = new_stock
    resp.safety_alert = False
    return resp

@router.post("/outbound", response_model=TransactionResultResponse, status_code=status.HTTP_201_CREATED)
async def outbound(
    data: OutboundTransactionCreate,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """출고 처리"""
    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    tx, new_stock, safety_alert = await inventory_service.process_outbound(db, data, user=None)
    
    resp = TransactionResultResponse.model_validate(tx)
    resp.new_stock = new_stock
    resp.safety_alert = safety_alert
    return resp

@router.post("/adjust", response_model=TransactionResultResponse, status_code=status.HTTP_201_CREATED)
async def adjust(
    data: AdjustTransactionCreate,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """재고 조정"""
    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    tx, new_stock, _ = await inventory_service.process_adjust(db, data, user=None)
    
    resp = TransactionResultResponse.model_validate(tx)
    resp.new_stock = new_stock
    return resp

@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    store_id: Optional[str] = None,
    product_id: Optional[str] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """트랜잭션 이력 조회"""
    s_id = None
    if store_id:
        try:
            s_id = UUID(store_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid store_id")
    
    p_id = None
    if product_id:
        try:
            p_id = UUID(product_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid product_id")

    items, total = await inventory_service.list_transactions(
        db, page=page, limit=limit, store_id=s_id, product_id=p_id, type=type
    )
    
    total_pages = (total + limit - 1) // limit
    
    return {
        "items": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": total_pages
        }
    }
