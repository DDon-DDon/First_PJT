from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.store import Store
from app.schemas.store import StoreResponse

router = APIRouter()

@router.get("", response_model=List[StoreResponse])
async def list_stores(db: AsyncSession = Depends(get_db)):
    """매장 목록 조회"""
    result = await db.execute(select(Store).order_by(Store.name))
    return result.scalars().all()
