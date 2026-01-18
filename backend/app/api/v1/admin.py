from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
# TODO: 인증 구현 후 활성화 (나중에 구현 예정)
# from app.api.deps import get_current_user
# from app.models.user import User, UserRole
from app.core.exceptions import ForbiddenException
from app.schemas.admin import LowStockItemResponse
from app.services import report as report_service

router = APIRouter()

@router.get("/alerts/low-stock", response_model=List[LowStockItemResponse])
async def get_low_stock_alerts(
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """안전재고 미만 알림 조회 (ADMIN)"""
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # if current_user.role != UserRole.ADMIN:
    #     raise ForbiddenException("Only ADMIN can view alerts")
        
    return await report_service.get_low_stock_items(db)

@router.get("/exports/low-stock")
async def export_low_stock(
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """안전재고 미만 목록 엑셀 다운로드 (ADMIN)"""
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # if current_user.role != UserRole.ADMIN:
    #     raise ForbiddenException("Only ADMIN can export data")
        
    items = await report_service.get_low_stock_items(db)
    excel_file = report_service.generate_low_stock_excel(items)
    
    filename = f"low_stock_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
