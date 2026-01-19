from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, nullable=False, unique=True)
    category_id = Column(Integer, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)