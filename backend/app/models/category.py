"""
🟢 GREEN: Category 모델 구현
"""
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class Category(Base):
    """
    제품 카테고리 모델

    예: SK(스킨케어), MU(메이크업), HC(헤어케어)
    """
    __tablename__ = "categories"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    # products: 해당 카테고리의 제품 목록

    def __repr__(self):
        return f"<Category {self.code}: {self.name}>"
