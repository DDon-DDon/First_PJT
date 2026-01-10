from typing import List, Optional, Tuple, Sequence
from uuid import UUID
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stock import CurrentStock
from app.models.product import Product
from app.models.user import User, UserRole
from app.models.user_store import UserStore
from app.models.transaction import InventoryTransaction, TransactionType
from app.schemas.transaction import (
    InboundTransactionCreate, OutboundTransactionCreate, AdjustTransactionCreate
)
from app.core.exceptions import ForbiddenException, InsufficientStockException

# ... (Previous functions: get_stock_status, get_current_stocks, get_product_stock_detail, _get_or_create_stock)
# To save context space, I will repeat the whole file content.

def get_stock_status(quantity: int, safety_stock: int) -> str:
    if quantity < safety_stock:
        return "LOW"
    elif quantity < safety_stock * 2:
        return "NORMAL"
    else:
        return "GOOD"

async def get_current_stocks(
    db: AsyncSession,
    user: User,
    page: int = 1,
    limit: int = 10,
    store_id: Optional[UUID] = None,
    category_id: Optional[UUID] = None,
    status: Optional[str] = None
) -> Tuple[Sequence[CurrentStock], int]:
    
    allowed_store_ids = []
    
    if user.role == UserRole.WORKER:
        stmt = select(UserStore.store_id).where(UserStore.user_id == user.id)
        result = await db.execute(stmt)
        allowed_store_ids = result.scalars().all()
        
        if not allowed_store_ids:
            return [], 0
            
        if store_id:
            if store_id not in allowed_store_ids:
                raise ForbiddenException("Access denied to this store")
            target_store_ids = [store_id]
        else:
            target_store_ids = allowed_store_ids
            
    else: # ADMIN
        target_store_ids = [store_id] if store_id else []

    query = select(CurrentStock).options(
        joinedload(CurrentStock.product),
        joinedload(CurrentStock.store)
    )

    if target_store_ids:
        query = query.where(CurrentStock.store_id.in_(target_store_ids))

    if category_id:
        query = query.join(Product).where(Product.category_id == category_id)
        
    if status:
        if not category_id:
            query = query.join(Product)
            
        if status == "LOW":
            query = query.where(CurrentStock.quantity < Product.safety_stock)
        elif status == "NORMAL":
            query = query.where(
                (CurrentStock.quantity >= Product.safety_stock) & 
                (CurrentStock.quantity < Product.safety_stock * 2)
            )
        elif status == "GOOD":
             query = query.where(CurrentStock.quantity >= Product.safety_stock * 2)

    subquery = query.subquery()
    count_stmt = select(func.count()).select_from(subquery)
    total = (await db.execute(count_stmt)).scalar_one()

    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    stocks = result.scalars().all()
    
    return stocks, total

async def get_product_stock_detail(
    db: AsyncSession,
    product_id: UUID,
    user: User
) -> Tuple[Optional[Product], Sequence[CurrentStock]]:
    if user.role != UserRole.ADMIN:
        raise ForbiddenException("Only ADMIN can view stock details")
    
    product = await db.get(Product, product_id)
    if not product:
        return None, []
        
    query = select(CurrentStock).options(
        joinedload(CurrentStock.store)
    ).where(CurrentStock.product_id == product_id)
    
    result = await db.execute(query)
    stocks = result.scalars().all()
    
    return product, stocks

async def list_transactions(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    store_id: Optional[UUID] = None,
    product_id: Optional[UUID] = None,
    type: Optional[str] = None
) -> Tuple[Sequence[InventoryTransaction], int]:
    
    query = select(InventoryTransaction).options(
        joinedload(InventoryTransaction.product),
        joinedload(InventoryTransaction.store),
        joinedload(InventoryTransaction.user)
    )
    
    if store_id:
        query = query.where(InventoryTransaction.store_id == store_id)
    if product_id:
        query = query.where(InventoryTransaction.product_id == product_id)
    if type:
        query = query.where(InventoryTransaction.type == type)
        
    query = query.order_by(InventoryTransaction.created_at.desc())
    
    # Count
    count_stmt = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_stmt)).scalar_one()
    
    # Paging
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return items, total

async def _get_or_create_stock(db: AsyncSession, product_id: UUID, store_id: UUID) -> CurrentStock:
    stmt = select(CurrentStock).options(
        joinedload(CurrentStock.product)
    ).where(
        CurrentStock.product_id == product_id,
        CurrentStock.store_id == store_id
    )
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    
    if not stock:
        stock = CurrentStock(product_id=product_id, store_id=store_id, quantity=0)
        db.add(stock)
        
    return stock

async def process_inbound(
    db: AsyncSession, 
    data: InboundTransactionCreate, 
    user: User
) -> Tuple[InventoryTransaction, int, bool]:
    stock = await _get_or_create_stock(db, UUID(data.productId), UUID(data.storeId))
    
    tx = InventoryTransaction(
        product_id=UUID(data.productId),
        store_id=UUID(data.storeId),
        user_id=user.id,
        type=TransactionType.INBOUND,
        quantity=data.quantity,
        note=data.note
    )
    db.add(tx)
    
    stock.quantity += data.quantity
    
    await db.commit()
    await db.refresh(tx)
    
    return tx, stock.quantity, False

async def process_outbound(
    db: AsyncSession, 
    data: OutboundTransactionCreate, 
    user: User
) -> Tuple[InventoryTransaction, int, bool]:
    p_id = UUID(data.productId)
    s_id = UUID(data.storeId)
    stock = await _get_or_create_stock(db, p_id, s_id)
    
    if stock.quantity < data.quantity:
        raise InsufficientStockException(
            detail=f"Not enough stock. Current: {stock.quantity}, Requested: {data.quantity}"
        )
        
    tx = InventoryTransaction(
        product_id=p_id,
        store_id=s_id,
        user_id=user.id,
        type=TransactionType.OUTBOUND,
        quantity=-data.quantity,
        note=data.note
    )
    db.add(tx)
    
    stock.quantity -= data.quantity
    
    await db.commit()
    await db.refresh(tx)
    
    if stock.product:
        safety = stock.product.safety_stock
    else:
        prod = await db.get(Product, p_id)
        safety = prod.safety_stock if prod else 0
            
    safety_alert = stock.quantity < safety
    
    return tx, stock.quantity, safety_alert

async def process_adjust(
    db: AsyncSession, 
    data: AdjustTransactionCreate, 
    user: User
) -> Tuple[InventoryTransaction, int, bool]:
    p_id = UUID(data.productId)
    s_id = UUID(data.storeId)
    stock = await _get_or_create_stock(db, p_id, s_id)
    
    if data.quantity < 0 and stock.quantity < abs(data.quantity):
         raise InsufficientStockException("Cannot reduce stock below 0")
         
    tx = InventoryTransaction(
        product_id=p_id,
        store_id=s_id,
        user_id=user.id,
        type=TransactionType.ADJUST,
        quantity=data.quantity,
        reason=data.reason,
        note=data.note
    )
    db.add(tx)
    
    stock.quantity += data.quantity
    
    await db.commit()
    await db.refresh(tx)
    
    return tx, stock.quantity, False
