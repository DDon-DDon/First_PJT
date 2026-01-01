from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """
    JWT Access Token 생성

    Args:
        subject: 토큰 주체 (일반적으로 user_id)
        expires_delta: 만료 시간 (기본값: 설정의 ACCESS_TOKEN_EXPIRE_MINUTES)

    Returns:
        str: 생성된 JWT 토큰
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """
    JWT Refresh Token 생성

    Args:
        subject: 토큰 주체 (일반적으로 user_id)
        expires_delta: 만료 시간 (기본값: 설정의 REFRESH_TOKEN_EXPIRE_DAYS)

    Returns:
        str: 생성된 JWT 토큰
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 검증

    Args:
        plain_password: 평문 비밀번호
        hashed_password: 해시된 비밀번호

    Returns:
        bool: 비밀번호 일치 여부
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    비밀번호 해싱

    Args:
        password: 평문 비밀번호

    Returns:
        str: 해시된 비밀번호
    """
    return pwd_context.hash(password)
