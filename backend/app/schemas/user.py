"""
사용자 스키마 정의 (User Schemas)

파일 역할:
    사용자 관련 API의 요청/응답 데이터 구조를 정의하는 Pydantic 스키마입니다.
    회원가입, 로그인, 사용자 정보 조회 등에 사용됩니다.

패턴:
    - DTO (Data Transfer Object) 패턴: API 계층과 모델 계층 분리
    - Request/Response 분리 패턴: 입력과 출력 스키마 구분
    - Validation 패턴: Pydantic Field로 입력값 검증
    - snake_case → camelCase 변환: 프론트엔드 JavaScript 규칙 준수

사용 목적:
    1. API 요청 데이터 검증 (자동 에러 처리)
    2. 안전한 응답 (password_hash 같은 민감 정보 제외)
    3. 명확한 API 문서 자동 생성
    4. ORM 모델과 API 계층 분리

작성일: 2026-01-01
TDD: Phase 1.2 - GREEN 단계에서 구현
"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """
    사용자 생성 요청 스키마 (회원가입)

    목적:
        회원가입 API의 요청 데이터를 검증합니다.
        필수 입력값과 검증 규칙을 정의합니다.

    사용 시나리오:
        - POST /api/users (회원가입)
        - POST /api/auth/register (회원가입 + 자동 로그인)

    Attributes:
        email (EmailStr): 이메일 (로그인 ID, 이메일 형식 자동 검증)
        password (str): 평문 비밀번호 (최소 6자, 서버에서 bcrypt 해싱)
        name (str): 사용자 이름 (1~100자)
        role (str): 역할 (WORKER 또는 ADMIN, 기본값: WORKER)

    검증 규칙:
        - email: EmailStr 타입 → "test@example.com" 형식 자동 검증
        - password: 최소 6자 이상 (min_length=6)
        - name: 최소 1자, 최대 100자 (min_length=1, max_length=100)
        - role: 기본값 "WORKER" (일반 사용자)

    예시:
        >>> # 요청 예시
        >>> {
        ...     "email": "worker@example.com",
        ...     "password": "password123",
        ...     "name": "홍길동",
        ...     "role": "WORKER"
        ... }

    주의사항:
        - password는 평문으로 받아서 서버에서 bcrypt 해싱
        - 응답에는 password 절대 포함 금지 (UserResponse 사용)
        - role은 추후 Enum으로 검증 강화 가능
    """
    email: EmailStr = Field(
        ...,  # 필수 필드
        description="이메일 (로그인 ID, 이메일 형식 검증)"
    )

    password: str = Field(
        ...,
        min_length=6,  # 최소 6자
        description="비밀번호 (최소 6자 이상, 서버에서 해싱)"
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="사용자 이름 (1~100자)"
    )

    role: str = Field(
        default="WORKER",  # 기본값: 일반 작업자
        description="역할 (WORKER 또는 ADMIN, 기본: WORKER)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "worker@donedone.local",
                "password": "worker123",
                "name": "홍길동",
                "role": "WORKER"
            }
        }
    }


class UserResponse(BaseModel):
    """
    사용자 응답 스키마

    목적:
        사용자 정보를 안전하게 클라이언트에게 제공합니다.
        민감한 정보(password_hash)는 제외하고 필요한 정보만 노출합니다.

    사용 시나리오:
        - GET /api/users/{id} (사용자 조회)
        - GET /api/users/me (내 정보 조회)
        - GET /api/users (사용자 목록)
        - POST /api/users (회원가입 성공 응답)

    Attributes:
        id (UUID): 사용자 고유 식별자
        email (EmailStr): 이메일
        name (str): 사용자 이름
        role (str): 역할 (WORKER 또는 ADMIN)
        isActive (bool): 활성화 여부 (False=비활성화/삭제된 사용자)
        createdAt (datetime): 가입일시
        updatedAt (datetime, optional): 최종 수정일시 (선택)

    Field Naming Convention:
        - Python 모델: snake_case (is_active, created_at)
        - API 응답: camelCase (isActive, createdAt)
        - model_config의 alias_generator로 자동 변환

    model_config:
        - from_attributes=True: SQLAlchemy 모델을 Pydantic 스키마로 자동 변환
          예: UserResponse.model_validate(user) → User 모델을 응답 스키마로 변환

    예시:
        >>> # 응답 예시
        >>> {
        ...     "id": "550e8400-e29b-41d4-a716-446655440000",
        ...     "email": "worker@example.com",
        ...     "name": "홍길동",
        ...     "role": "WORKER",
        ...     "isActive": true,
        ...     "createdAt": "2026-01-01T09:00:00",
        ...     "updatedAt": "2026-01-02T10:00:00"
        ... }

        >>> # ORM 모델 → 응답 스키마 변환
        >>> user = await session.get(User, user_id)
        >>> response = UserResponse.model_validate(user)

    주의사항:
        - password_hash 절대 포함 금지 (보안)
        - from_attributes=True로 ORM 객체 직접 변환 가능
        - updatedAt은 Optional (수정 없으면 None)
    """
    id: UUID = Field(
        ...,
        description="사용자 고유 식별자 (UUID)"
    )

    email: EmailStr = Field(
        ...,
        description="이메일"
    )

    name: str = Field(
        ...,
        description="사용자 이름"
    )

    role: str = Field(
        ...,
        description="역할 (WORKER 또는 ADMIN)"
    )

    isActive: bool = Field(
        ...,
        description="활성화 여부 (False=비활성화/삭제된 사용자)"
    )

    createdAt: datetime = Field(
        ...,
        description="가입일시 (UTC)"
    )

    updatedAt: Optional[datetime] = Field(
        None,  # 선택 필드 (수정 없으면 None)
        description="최종 수정일시 (UTC, 수정 없으면 null)"
    )

    # Pydantic v2 설정
    model_config = {
        "from_attributes": True  # SQLAlchemy 모델 → Pydantic 스키마 자동 변환
    }
