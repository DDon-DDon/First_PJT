from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.store import Store
from app.schemas.store import StoreResponse, StoreCreate

router = APIRouter()

@router.get(
    "",
    response_model=List[StoreResponse],
    summary="매장 목록 조회",
    description="""
    등록된 모든 매장 목록을 조회합니다.

    - 매장명 기준 오름차순 정렬
    - 인증 없이 접근 가능 (공개 API)
    """,
    responses={
        200: {
            "description": "매장 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "660e8400-e29b-41d4-a716-446655440000",
                            "code": "GN001",
                            "name": "강남점",
                            "address": "서울시 강남구 테헤란로 123",
                            "phone": "02-1234-5678",
                            "isActive": True
                        }
                    ]
                }
            }
        }
    }
)
async def list_stores(db: AsyncSession = Depends(get_db)):
    """매장 목록 조회"""
    result = await db.execute(select(Store).order_by(Store.name))
    return result.scalars().all()

@router.post("", response_model=StoreResponse, status_code=201)
async def create_store(store_in: StoreCreate, db: AsyncSession = Depends(get_db)):
    """매장 생성"""
    # Check for duplicate code
    existing = await db.execute(select(Store).where(Store.code == store_in.code))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Store with this code already exists")

    store = Store(**store_in.model_dump(by_alias=False))
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store
