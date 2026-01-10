from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.inventory import StockListResponse, StockItemResponse
from app.services import inventory as inventory_service

router = APIRouter()

@router.get("/stocks", response_model=StockListResponse)
async def list_stocks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    store_id: Optional[str] = None,
    category_id: Optional[str] = None,
    status: Optional[str] = Query(None, regex="^(LOW|NORMAL|GOOD)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    stocks, total = await inventory_service.get_current_stocks(
        db,
        user=current_user,
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

@router.get("/stocks/{product_id}", response_model=ProductStockDetailResponse)
async def get_product_stock_detail(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """제품별 매장 재고 조회 (ADMIN Only)"""
    try:
        p_id = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product_id")

    product, stocks = await inventory_service.get_product_stock_detail(
        db, p_id, current_user
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
