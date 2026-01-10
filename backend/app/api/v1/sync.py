from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.sync import SyncRequest, SyncResponse
from app.services import sync as sync_service

router = APIRouter()

@router.post("/transactions", response_model=SyncResponse)
async def sync_transactions(
    request: SyncRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """오프라인 트랜잭션 동기화"""
    return await sync_service.sync_transactions(db, request, current_user)
