"""
🟢 GREEN: InventoryTransaction 모델 구현
"""
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class TransactionType(str, enum.Enum):
    """트랜잭션 유형"""
    INBOUND = "INBOUND"   # 입고
    OUTBOUND = "OUTBOUND" # 출고
    ADJUST = "ADJUST"     # 조정


class AdjustReason(str, enum.Enum):
    """조정 사유"""
    EXPIRED = "EXPIRED"       # 유통기한 만료
    DAMAGED = "DAMAGED"       # 파손
    CORRECTION = "CORRECTION" # 재고 정정
    OTHER = "OTHER"           # 기타


class InventoryTransaction(Base):
    """
    재고 트랜잭션 모델 (Append-Only)

    모든 입출고 이력을 기록하는 원장
    """
    __tablename__ = "inventory_transactions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    product_id = Column(GUID, ForeignKey("products.id"), nullable=False)
    store_id = Column(GUID, ForeignKey("stores.id"), nullable=False)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    quantity = Column(Integer, nullable=False)  # 양수: 입고, 음수: 출고/조정
    reason = Column(SQLEnum(AdjustReason))      # 조정 시 사유
    note = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    synced_at = Column(DateTime)  # 동기화 완료 시각 (NULL이면 동기화 대기)

    # Relationships
    product = relationship("Product", backref="transactions")
    store = relationship("Store", backref="transactions")
    user = relationship("User", backref="transactions")

    def __repr__(self):
        return f"<Transaction {self.type} {self.quantity} at {self.created_at}>"
