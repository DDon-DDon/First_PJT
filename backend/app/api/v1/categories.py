from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryResponse, CategoryCreate

router = APIRouter()

@router.get(
    "",
    response_model=List[CategoryResponse],
    summary="카테고리 목록 조회",
    description="""
    등록된 모든 카테고리 목록을 조회합니다.

    - 정렬 순서(`sortOrder`) 기준 오름차순 정렬
    - 인증 없이 접근 가능 (공개 API)
    """,
    responses={
        200: {
            "description": "카테고리 목록 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "770e8400-e29b-41d4-a716-446655440000",
                            "code": "SNACK",
                            "name": "스낵",
                            "sortOrder": 1
                        },
                        {
                            "id": "780e8400-e29b-41d4-a716-446655440000",
                            "code": "DRINK",
                            "name": "음료",
                            "sortOrder": 2
                        }
                    ]
                }
            }
        }
    }
)
async def list_categories(db: AsyncSession = Depends(get_db)):
    """카테고리 목록 조회"""
    result = await db.execute(select(Category).order_by(Category.sort_order))
    return result.scalars().all()

@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """카테고리 생성"""
    existing = await db.execute(select(Category).where(Category.code == category_in.code))
    if existing.scalar_one_or_none():
         raise HTTPException(status_code=400, detail="Category with this code already exists")

    # Manual mapping to be safe or use by_alias=False
    # Since schema uses camelCase alias "sortOrder" but DB expects "sort_order"
    category = Category(
        code=category_in.code,
        name=category_in.name,
        sort_order=category_in.sort_order
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
