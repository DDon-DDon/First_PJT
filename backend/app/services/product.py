from typing import Optional, List, Tuple, Sequence
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate
from app.core.exceptions import ConflictException, NotFoundException

async def get_product_by_barcode(db: AsyncSession, barcode: str) -> Optional[Product]:
    """
    바코드로 제품 조회
    """
    stmt = select(Product).options(joinedload(Product.category)).where(Product.barcode == barcode)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def list_products(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    category_id: Optional[UUID] = None
) -> Tuple[Sequence[Product], int]:
    """
    제품 목록 조회 (페이지네이션, 검색, 필터)
    Returns: (items, total_count)
    """
    # 기본 쿼리
    query = select(Product).options(joinedload(Product.category))

    # 필터링
    if category_id:
        query = query.where(Product.category_id == category_id)
    
    if search:
        # 이름 또는 바코드 검색 (대소문자 무시)
        query = query.where(
            (Product.name.ilike(f"%{search}%")) | 
            (Product.barcode.ilike(f"%{search}%"))
        )
    
    # 정렬 (최신순)
    query = query.order_by(Product.created_at.desc())

    # 전체 개수 계산 (별도 쿼리)
    # count_query = select(func.count()).select_from(query.subquery()) # subquery 방식
    # 더 효율적인 방식:
    count_stmt = select(func.count(Product.id))
    if category_id:
        count_stmt = count_stmt.where(Product.category_id == category_id)
    if search:
        count_stmt = count_stmt.where(
            (Product.name.ilike(f"%{search}%")) | 
            (Product.barcode.ilike(f"%{search}%"))
        )
    
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    # 페이지네이션
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    items = result.scalars().all()

    return items, total

async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    """
    제품 생성
    """
    # 1. 바코드 중복 체크
    existing = await get_product_by_barcode(db, data.barcode)
    if existing:
        raise ConflictException(f"Product with barcode {data.barcode} already exists")

    # 2. 카테고리 존재 확인 (Optional but good for explicit error)
    # Pydantic schema takes string UUID, need to convert
    try:
        cat_id = UUID(data.category_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category ID format")
        
    category_stmt = select(Category).where(Category.id == cat_id)
    category_res = await db.execute(category_stmt)
    if not category_res.scalar_one_or_none():
         raise NotFoundException(f"Category {data.category_id} not found")

    # 3. 생성
    product = Product(
        barcode=data.barcode,
        name=data.name,
        category_id=cat_id,
        safety_stock=data.safety_stock,
        image_url=data.image_url,
        memo=data.memo
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return product

