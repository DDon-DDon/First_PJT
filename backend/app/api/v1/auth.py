"""
인증 API 라우터 (Auth Router)

파일 역할:
    사용자 인증 관련 엔드포인트 (로그인, 회원가입 등)
    현재는 플레이스홀더로, 추후 JWT 인증 구현 예정

작성일: 2026-01-30
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_current_user():
    """
    현재 로그인한 사용자 정보 조회 (Placeholder)
    
    TODO: JWT 토큰 검증 후 사용자 정보 반환
    """
    return {
        "message": "Auth endpoint placeholder",
        "note": "JWT 인증 구현 예정"
    }
