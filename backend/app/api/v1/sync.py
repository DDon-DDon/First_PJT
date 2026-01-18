from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
# TODO: 인증 구현 후 활성화 (나중에 구현 예정)
# from app.api.deps import get_current_user
# from app.models.user import User
from app.schemas.sync import SyncRequest, SyncResponse
from app.services import sync as sync_service

router = APIRouter()

@router.post("/transactions", response_model=SyncResponse)
async def sync_transactions(
    request: SyncRequest,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """오프라인 트랜잭션 동기화"""
    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    return await sync_service.sync_transactions(db, request, user=None)
