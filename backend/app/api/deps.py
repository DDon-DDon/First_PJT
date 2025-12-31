from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.db.session import get_db

# OAuth2 스키마 정의
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme)
) -> str:
    """
    JWT 토큰에서 현재 사용자 ID 추출

    Args:
        token: JWT 액세스 토큰

    Returns:
        str: 사용자 ID (UUID)

    Raises:
        UnauthorizedException: 토큰이 유효하지 않은 경우
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("Could not validate credentials")
        return user_id
    except JWTError:
        raise UnauthorizedException("Could not validate credentials")


# TODO: User 모델 구현 후 활성화
# from app.models.user import User
# from sqlalchemy import select

# async def get_current_user(
#     db: AsyncSession = Depends(get_db),
#     user_id: str = Depends(get_current_user_id)
# ) -> User:
#     """
#     현재 인증된 사용자 정보 조회
#
#     Args:
#         db: 데이터베이스 세션
#         user_id: 사용자 ID
#
#     Returns:
#         User: 사용자 모델 인스턴스
#
#     Raises:
#         UnauthorizedException: 사용자를 찾을 수 없는 경우
#     """
#     result = await db.execute(
#         select(User).where(User.id == user_id)
#     )
#     user = result.scalar_one_or_none()
#
#     if not user:
#         raise UnauthorizedException("User not found")
#
#     return user
