from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
# TODO: 인증 구현 후 활성화 (나중에 구현 예정)
# from app.api.deps import get_current_user
# from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductListResponse
from app.services import product as product_service
from app.core.exceptions import ForbiddenException

router = APIRouter()

@router.get(
    "/barcode/{barcode}",
    response_model=ProductResponse,
    summary="바코드 스캔 제품 조회",
    description="""
    바코드 번호로 제품 정보를 조회합니다.

    - **Unique Index**를 활용하여 대량의 데이터에서도 빠른 조회가 가능합니다.
    - 바코드 스캐너 연동 시 사용됩니다.
    """,
    responses={
        404: {"description": "해당 바코드의 제품이 존재하지 않음"}
    }
)
async def get_product_by_barcode(
    barcode: str,
    db: AsyncSession = Depends(get_db)
):
    product = await product_service.get_product_by_barcode(db, barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get(
    "",
    response_model=ProductListResponse,
    summary="제품 목록 조회 (검색/필터)",
    description="""
    제품 목록을 페이지네이션하여 조회합니다.

    - **검색(`search`)**: 제품명 또는 바코드에 검색어가 포함된 제품을 찾습니다.
    - **카테고리(`category_id`)**: 특정 카테고리의 제품만 필터링합니다.
    - **정렬**: 최신 등록순으로 정렬됩니다.
    """
)
async def list_products(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    search: Optional[str] = Query(None, description="검색어 (제품명/바코드)"),
    category_id: Optional[str] = Query(None, description="카테고리 필터 (UUID)"),
    db: AsyncSession = Depends(get_db)
):
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

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="신규 제품 등록 (관리자)",
    description="""
    새로운 제품을 시스템에 등록합니다.

    - **권한**: `ADMIN` 권한이 있는 사용자만 가능합니다.
    - **바코드**: 이미 존재하는 바코드는 등록할 수 없습니다 (409 Conflict).
    """,
    responses={
        403: {"description": "권한 없음 (Worker 접근 불가)"},
        409: {"description": "이미 존재하는 바코드"},
        400: {"description": "잘못된 카테고리 ID"}
    }
)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """제품 등록 (관리자 전용)"""
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # if current_user.role != "ADMIN":
    #     raise ForbiddenException("Only ADMIN can create products")

    return await product_service.create_product(db, data)
