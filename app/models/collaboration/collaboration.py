from sqlalchemy import Column, Integer, Boolean, Text, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship


class Collaboration(Base):
    __tablename__ = "collaboration"

    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, unique=True, nullable=False)
    logo = Column(Text, nullable=False)
    website_url = Column(Text, nullable=True)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    translations = relationship("CollaborationTranslation", back_populates="collaboration", cascade="all, delete")
