"""
🟢 GREEN: Product 모델 구현
"""
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class Product(Base):
    """
    제품 마스터 모델

    바코드 기반으로 제품을 식별하고 관리
    """
    __tablename__ = "products"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    barcode = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(GUID, ForeignKey("categories.id"), nullable=False)
    safety_stock = Column(Integer, nullable=False, default=10)
    image_url = Column(String(500))
    memo = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("Category", backref="products")
    # stocks: 현재고 목록
    # transactions: 트랜잭션 목록

    def __repr__(self):
        return f"<Product {self.barcode}: {self.name}>"
