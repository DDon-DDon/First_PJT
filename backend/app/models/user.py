"""
🟢 GREEN: User 모델 구현
"""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class UserRole(str, enum.Enum):
    """사용자 역할"""
    WORKER = "WORKER"
    ADMIN = "ADMIN"


class User(Base):
    """
    사용자 모델

    - WORKER: 일반 작업자 (배정된 매장만 접근)
    - ADMIN: 관리자 (모든 매장 접근 + 관리 기능)
    """
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.WORKER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    # stores: 배정된 매장 목록 (user_stores를 통해)
    # transactions: 작성한 트랜잭션 목록

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
