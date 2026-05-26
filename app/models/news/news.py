from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean, JSON

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, nullable=False, unique=True)
    category_id = Column(Integer, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    show_in_all_news = Column(Boolean, nullable=False, default=True, server_default="true")
    sdg_numbers = Column(JSON, nullable=True)
    faculty_code = Column(String(50), nullable=True)
    cafedra_code = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))
