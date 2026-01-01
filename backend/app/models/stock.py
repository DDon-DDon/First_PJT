"""
🟢 GREEN: CurrentStock 모델 구현
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from app.db.types import GUID


class CurrentStock(Base):
    """
    현재고 모델 (캐시)

    빠른 재고 조회를 위한 캐시 테이블
    실제 재고는 InventoryTransaction의 합계로 계산
    """
    __tablename__ = "current_stocks"

    product_id = Column(GUID, ForeignKey("products.id"), primary_key=True)
    store_id = Column(GUID, ForeignKey("stores.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)
    last_alerted_at = Column(DateTime)  # 마지막 안전재고 알림 시각
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", backref="stocks")
    store = relationship("Store", backref="stocks")

    def __repr__(self):
        return f"<CurrentStock product={self.product_id} store={self.store_id} qty={self.quantity}>"
