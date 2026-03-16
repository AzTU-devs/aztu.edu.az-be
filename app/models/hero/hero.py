from app.core.database import Base
from sqlalchemy import Column, Integer, Text, DateTime, Boolean


class Hero(Base):
    __tablename__ = "hero"

    id = Column(Integer, primary_key=True, index=True)
    hero_id = Column(Integer, nullable=False, unique=True)
    video = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))
