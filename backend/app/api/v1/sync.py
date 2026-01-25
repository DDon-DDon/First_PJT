from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
# TODO: 인증 구현 후 활성화 (나중에 구현 예정)
# from app.api.deps import get_current_user
# from app.models.user import User
from app.schemas.sync import SyncRequest, SyncResponse
from app.schemas.common import ErrorResponse
from app.services import sync as sync_service

router = APIRouter()

@router.post(
    "/transactions",
    response_model=SyncResponse,
    summary="오프라인 트랜잭션 일괄 동기화",
    description="""
    오프라인에서 수집된 트랜잭션들을 서버에 일괄 동기화합니다.

    - 각 트랜잭션은 `localId`로 식별됩니다.
    - 성공한 항목: `synced` 배열에 `localId` → `serverId` 매핑 반환
    - 실패한 항목: `failed` 배열에 `localId`와 에러 메시지 반환
    - 부분 성공이 가능합니다 (일부만 실패해도 나머지는 처리됨).
    """,
    responses={
        200: {
            "description": "동기화 처리 완료 (부분 실패 포함 가능)",
            "content": {
                "application/json": {
                    "example": {
                        "synced": [
                            {
                                "localId": "110e8400-e29b-41d4-a716-446655440000",
                                "serverId": "880e8400-e29b-41d4-a716-446655440000"
                            }
                        ],
                        "failed": [
                            {
                                "localId": "220e8400-e29b-41d4-a716-446655440000",
                                "error": "재고 부족: 현재 5개, 요청 10개"
                            }
                        ],
                        "syncedAt": "2026-01-24T10:00:00Z"
                    }
                }
            }
        },
        401: {
            "model": ErrorResponse,
            "description": "인증 필요"
        }
    }
)
async def sync_transactions(
    request: SyncRequest,
    db: AsyncSession = Depends(get_db)
    # TODO: 인증 구현 후 활성화 (나중에 구현 예정)
    # current_user: User = Depends(get_current_user)
):
    """오프라인 트랜잭션 동기화"""
    # TODO: 인증 구현 후 활성화 - 현재는 user=None으로 처리
    return await sync_service.sync_transactions(db, request, user=None)
