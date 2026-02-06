from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
# TODO: 인증 구현 후 활성화 (나중에 구현 예정)
# from app.api.deps import get_current_user
# from app.models.user import User
from app.schemas.inventory import StockListResponse, StockItemResponse
from app.schemas.common import ErrorResponse
from app.services import inventory as inventory_service

router = APIRouter()

@router.get(
    "/stocks",
    response_model=StockListResponse,
    summary="현재고 목록 조회",
    description="""
    매장별 현재고 목록을 페이지네이션하여 조회합니다.

    - **매장 필터(`store_id`)**: 특정 매장의 재고만 조회
    - **카테고리 필터(`category_id`)**: 특정 카테고리의 제품만 조회
    - **상태 필터(`status`)**: LOW(안전재고 미달), NORMAL, GOOD 중 선택
    """,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "잘못된 요청 파라미터",
            "content": {
                "application/json": {
                    "example": {
                        "code": "INVALID_STORE_ID",
                        "message": "매장 ID 형식이 올바르지 않습니다",
                        "details": {"store_id": "invalid-uuid"}
                    }
                }
            }
        }
    }
)
async def list_stocks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    store_id: Optional[str] = None,
    category_id: Optional[str] = None,
    status: Optional[str] = Query(None, regex="^(LOW|NORMAL|GOOD)$"),
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """현재고 목록 조회"""
    
    # UUID 변환
    s_id = None
    if store_id:
        try:
            s_id = UUID(store_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid store_id")
            
    c_id = None
    if category_id:
        try:
            c_id = UUID(category_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid category_id")

    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    stocks, total = await inventory_service.get_current_stocks(
        db,
        user=None,  # TODO: current_user로 변경 필요
        page=page,
        limit=limit,
        store_id=s_id,
        category_id=c_id,
        status=status
    )
    
    # 응답 변환 (status 계산 포함)
    items = []
    for stock in stocks:
        stock_status = inventory_service.get_stock_status(
            stock.quantity, 
            stock.product.safety_stock
        )
        
        # Pydantic 모델로 변환 (status 주입)
        # StockItemResponse는 ORM 객체 + status 필드를 원함
        # dictionary로 만들어서 validate
        item_dict = {
            "product": stock.product,
            "store": stock.store,
            "quantity": stock.quantity,
            "status": stock_status,
            "lastAlertedAt": stock.last_alerted_at
        }
        items.append(StockItemResponse.model_validate(item_dict))

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

from app.schemas.inventory import ProductStockDetailResponse

@router.get(
    "/stocks/{product_id}",
    response_model=ProductStockDetailResponse,
    summary="제품별 매장 재고 상세 조회",
    description="""
    특정 제품의 모든 매장 재고를 조회합니다.

    - **ADMIN**: 모든 매장의 재고 조회 가능
    - **WORKER**: 본인이 소속된 매장의 재고만 조회 가능
    """,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "잘못된 제품 ID",
            "content": {
                "application/json": {
                    "example": {
                        "code": "INVALID_PRODUCT_ID",
                        "message": "제품 ID 형식이 올바르지 않습니다",
                        "details": {"product_id": "invalid-uuid"}
                    }
                }
            }
        },
        404: {
            "model": ErrorResponse,
            "description": "제품을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "code": "PRODUCT_NOT_FOUND",
                        "message": "해당 제품을 찾을 수 없습니다",
                        "details": {"product_id": "550e8400-e29b-41d4-a716-446655440000"}
                    }
                }
            }
        }
    }
)
async def get_product_stock_detail(
    product_id: str,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """제품별 매장 재고 조회 (ADMIN Only)"""
    try:
        p_id = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product_id")

    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    product, stocks = await inventory_service.get_product_stock_detail(
        db, p_id, user=None  # TODO: current_user로 변경 필요
    )
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    stock_items = []
    total_qty = 0
    
    for stock in stocks:
        status = inventory_service.get_stock_status(stock.quantity, product.safety_stock)
        
        # Pydantic 모델 변환
        # product 정보는 이미 조회했으므로 재사용
        # store는 joinedload로 로딩됨
        item_dict = {
            "product": product,
            "store": stock.store,
            "quantity": stock.quantity,
            "status": status,
            "lastAlertedAt": stock.last_alerted_at
        }
        stock_items.append(StockItemResponse.model_validate(item_dict))
        total_qty += stock.quantity
        
    return {
        "product": product,
        "stocks": stock_items,
        "totalQuantity": total_qty
    }
