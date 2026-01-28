from app.core.database import Base
from sqlalchemy import Column, Integer, Text, DateTime, Boolean

class Collaboration(Base):
    __tablename__ = "collaboration"

    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, nullable=False, unique=True)
    display_order = Column(Integer, nullable=False)
    image = Column(Text, nullable=False)
    url = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)