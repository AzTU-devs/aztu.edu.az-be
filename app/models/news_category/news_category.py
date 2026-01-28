from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean

class NewsCategory(Base):
    __tablename__ = "news_category"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)