"""
사용자 모델 (User Model)

파일 역할:
    시스템 사용자의 정보를 관리하는 SQLAlchemy ORM 모델입니다.
    로그인, 권한 관리, 사용자 정보 저장을 담당합니다.

패턴:
    - Active Record 패턴: SQLAlchemy ORM을 통한 DB 접근
    - Enum 패턴: UserRole로 역할 타입 안전성 보장
    - Soft Delete 패턴: is_active로 논리적 삭제

작성일: 2026-01-01
TDD: Phase 1.1 - GREEN 단계에서 구현
"""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class UserRole(str, enum.Enum):
    """
    사용자 역할 열거형

    목적:
        사용자의 권한 수준을 명확하게 정의하고 타입 안전성을 보장합니다.

    값:
        WORKER: 일반 작업자
            - 배정된 매장에서만 작업 가능
            - 입출고 처리, 재고 조회 권한
            - 제품 등록/수정/삭제 불가
        ADMIN: 관리자
            - 모든 매장 접근 가능
            - 제품 등록/수정/삭제 가능
            - 사용자 관리, 매장 관리 권한

    사용 이유:
        - 문자열 하드코딩 방지 ("WORKER" 오타 → "WROKER" 에러 방지)
        - IDE 자동완성 지원
        - DB에서 ENUM 타입으로 저장 → 잘못된 값 입력 방지

    예시:
        >>> user.role = UserRole.WORKER
        >>> if user.role == UserRole.ADMIN:
        ...     # 관리자 전용 기능
    """
    WORKER = "WORKER"  # 일반 작업자
    ADMIN = "ADMIN"  # 관리자


class User(Base):
    """
    사용자 모델 (Users 테이블)

    목적:
        시스템에 로그인하는 사용자의 정보를 저장하고 관리합니다.
        JWT 인증, 권한 체크, 트랜잭션 이력 추적에 사용됩니다.

    비즈니스 규칙:
        1. 이메일은 유니크 (중복 불가)
        2. 비밀번호는 해싱되어 저장 (bcrypt 사용)
        3. 기본 역할은 WORKER
        4. 삭제 시 is_active=False로 비활성화 (Soft Delete)

    관계:
        - UserStore (N:M): 여러 매장에 배정 가능
        - InventoryTransaction (1:N): 작성한 트랜잭션 목록

    Attributes:
        id (GUID): 고유 식별자 (UUID v4)
        email (str): 로그인 이메일 (유니크, 인덱스)
        password_hash (str): bcrypt 해싱된 비밀번호
        name (str): 사용자 이름
        role (UserRole): 역할 (WORKER 또는 ADMIN)
        is_active (bool): 활성화 여부 (Soft Delete용)
        created_at (datetime): 가입일
        updated_at (datetime): 최종 수정일

    예시:
        >>> # 사용자 생성
        >>> user = User(
        ...     email="worker@example.com",
        ...     password_hash=bcrypt.hashpw(password, salt),
        ...     name="홍길동",
        ...     role=UserRole.WORKER
        ... )
        >>> session.add(user)
        >>> await session.commit()

        >>> # 조회
        >>> user = await session.get(User, user_id)
        >>> if user.is_active and user.role == UserRole.ADMIN:
        ...     # 관리자 권한 필요한 작업
    """

    # 테이블 이름
    __tablename__ = "users"

    # Primary Key
    id = Column(
        GUID,  # PostgreSQL: UUID, SQLite: CHAR(32)
        primary_key=True,
        default=uuid.uuid4,  # 자동으로 UUID v4 생성
        comment="사용자 고유 식별자"
    )

    # 인증 정보
    email = Column(
        String(255),
        unique=True,  # 중복 불가 (UNIQUE 제약조건)
        nullable=False,  # NULL 불가
        index=True,  # 로그인 속도 향상을 위한 인덱스
        comment="로그인 이메일 주소"
    )

    password_hash = Column(
        String(255),
        nullable=False,
        comment="bcrypt 해싱된 비밀번호 (평문 저장 절대 금지)"
    )

    # 사용자 정보
    name = Column(
        String(100),
        nullable=False,
        comment="사용자 이름"
    )

    role = Column(
        SQLEnum(UserRole),  # ENUM 타입으로 저장
        nullable=False,
        default=UserRole.WORKER,  # 기본값: WORKER
        comment="사용자 역할 (WORKER 또는 ADMIN)"
    )

    # 상태 관리
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,  # 기본값: 활성화
        comment="활성화 여부 (False=비활성화/삭제된 사용자)"
    )

    # 타임스탬프
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,  # 생성 시 자동으로 현재 시각
        comment="가입일시"
    )

    updated_at = Column(
        DateTime,
        onupdate=datetime.utcnow,  # 수정 시 자동으로 현재 시각
        comment="최종 수정일시"
    )

    # Relationships (실제 컬럼 아님, ORM 편의 기능)
    stores = relationship(
        "Store",
        secondary="user_stores",
        backref="users",
        lazy="selectin"
    )
    
    # transactions: 작성한 트랜잭션 목록
    #   - relationship 정의는 추후 추가 예정
    #   - 예: user.transactions → [InventoryTransaction, ...]

    def __repr__(self):
        """
        개발/디버깅용 문자열 표현

        Returns:
            str: <User email (role)> 형식

        예시:
            >>> print(user)
            <User worker@example.com (WORKER)>
        """
        return f"<User {self.email} ({self.role.value})>"

    # 비즈니스 로직 메서드 (추후 추가 예정)
    #
    # def check_password(self, password: str) -> bool:
    #     """비밀번호 검증"""
    #     return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    #
    # def has_access_to_store(self, store_id: UUID) -> bool:
    #     """특정 매장 접근 권한 체크"""
    #     if self.role == UserRole.ADMIN:
    #         return True  # 관리자는 모든 매장 접근 가능
    #     return store_id in [s.id for s in self.stores]
