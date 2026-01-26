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
from app.schemas.common import ErrorResponse
from app.services import inventory as inventory_service

router = APIRouter()

@router.post(
    "/inbound",
    response_model=TransactionResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="입고 처리",
    description="""
    제품을 매장에 입고합니다.

    - 입고 수량만큼 현재고가 증가합니다.
    - 트랜잭션 이력이 기록됩니다.
    """,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "제품 또는 매장을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "code": "PRODUCT_NOT_FOUND",
                        "message": "해당 제품을 찾을 수 없습니다",
                        "details": None
                    }
                }
            }
        }
    }
)
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

@router.post(
    "/outbound",
    response_model=TransactionResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="출고 처리",
    description="""
    제품을 매장에서 출고합니다.

    - 출고 수량만큼 현재고가 감소합니다.
    - 재고가 안전재고 미만이 되면 `safetyAlert: true`가 반환됩니다.
    - 재고 부족 시 400 에러가 발생합니다.
    """,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "재고 부족",
            "content": {
                "application/json": {
                    "example": {
                        "code": "STOCK_INSUFFICIENT",
                        "message": "재고가 부족합니다",
                        "details": {"available": 5, "requested": 10}
                    }
                }
            }
        },
        404: {
            "model": ErrorResponse,
            "description": "제품 또는 매장을 찾을 수 없음"
        }
    }
)
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

@router.post(
    "/adjust",
    response_model=TransactionResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="재고 조정",
    description="""
    재고를 직접 조정합니다 (분실, 파손, 만료 등).

    - 양수: 재고 증가 (예: 반품)
    - 음수: 재고 감소 (예: 분실, 파손)
    - 조정 사유(`reason`)는 필수입니다: DAMAGED, LOST, EXPIRED, RETURN, OTHER
    """,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "잘못된 조정 요청",
            "content": {
                "application/json": {
                    "example": {
                        "code": "INVALID_ADJUSTMENT",
                        "message": "조정 후 재고가 음수가 됩니다",
                        "details": {"current": 5, "adjustment": -10}
                    }
                }
            }
        }
    }
)
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

@router.get(
    "",
    response_model=TransactionListResponse,
    summary="트랜잭션 이력 조회",
    description="""
    입고/출고/조정 트랜잭션 이력을 조회합니다.

    - **매장 필터(`store_id`)**: 특정 매장의 이력만 조회
    - **제품 필터(`product_id`)**: 특정 제품의 이력만 조회
    - **타입 필터(`type`)**: INBOUND, OUTBOUND, ADJUST 중 선택
    - 최신순으로 정렬됩니다.
    """,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "잘못된 요청 파라미터"
        }
    }
)
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
