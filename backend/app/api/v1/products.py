from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductListResponse
from app.schemas.common import Pagination
from app.services import product as product_service
from app.core.exceptions import ForbiddenException

router = APIRouter()

@router.get("/barcode/{barcode}", response_model=ProductResponse)
async def get_product_by_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_db)
):
    """바코드로 제품 조회"""
    product = await product_service.get_product_by_barcode(db, barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[str] = None, # Query param is string, convert to UUID
    db: AsyncSession = Depends(get_db)
):
    """제품 목록 조회"""
    cat_id = None
    if category_id:
        try:
            cat_id = UUID(category_id)
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid category_id format")

    items, total = await product_service.list_products(
        db, page=page, limit=limit, search=search, category_id=cat_id
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

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """제품 등록 (관리자 전용)"""
    if current_user.role != "ADMIN":
        raise ForbiddenException("Only ADMIN can create products")
        
    return await product_service.create_product(db, data)
