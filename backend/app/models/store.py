"""
🟢 GREEN: Store 모델 구현
"""
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class Store(Base):
    """
    매장/창고 모델

    재고를 보관하는 물리적 장소
    """
    __tablename__ = "stores"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(500))
    phone = Column(String(20))
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    # users: 배정된 사용자 목록 (user_stores를 통해)
    # stocks: 현재고 목록
    # transactions: 트랜잭션 목록

    def __repr__(self):
        return f"<Store {self.code}: {self.name}>"
