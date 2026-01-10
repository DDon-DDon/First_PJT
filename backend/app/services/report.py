from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO
from openpyxl import Workbook

from app.models.stock import CurrentStock
from app.models.product import Product
from app.schemas.admin import LowStockItemResponse

class LowStockItemDTO:
    def __init__(self, product, store, quantity, safety_stock):
        self.product = product
        self.store = store
        self.current_stock = quantity
        self.shortage = safety_stock - quantity

async def get_low_stock_items(db: AsyncSession) -> List[LowStockItemDTO]:
    stmt = select(CurrentStock).options(
        joinedload(CurrentStock.product),
        joinedload(CurrentStock.store)
    ).join(Product).where(
        CurrentStock.quantity < Product.safety_stock
    )
    
    result = await db.execute(stmt)
    stocks = result.scalars().all()
    
    items = []
    for s in stocks:
        items.append(LowStockItemDTO(
            product=s.product,
            store=s.store,
            quantity=s.quantity,
            safety_stock=s.product.safety_stock
        ))
    return items

def generate_low_stock_excel(items: List[LowStockItemDTO]) -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Low Stock"
    
    # Headers
    ws.append(["제품명", "바코드", "매장명", "현재고", "안전재고", "부족수량"])
    
    # Data
    for item in items:
        ws.append([
            item.product.name,
            item.product.barcode,
            item.store.name,
            item.current_stock,
            item.product.safety_stock,
            item.shortage
        ])
    
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output
