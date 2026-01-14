from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    func,
    Boolean
)
from app.core.database import Base
from sqlalchemy.orm import relationship

class Announcement(Base):
    __tablename__ = "announcement"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, nullable=False, unique=True)
    image = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())