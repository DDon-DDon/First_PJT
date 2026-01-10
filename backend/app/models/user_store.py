from sqlalchemy import Column, DateTime, ForeignKey
from datetime import datetime

from app.db.base import Base
from app.db.types import GUID

class UserStore(Base):
    __tablename__ = "user_stores"

    user_id = Column(GUID, ForeignKey("users.id"), primary_key=True)
    store_id = Column(GUID, ForeignKey("stores.id"), primary_key=True)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
