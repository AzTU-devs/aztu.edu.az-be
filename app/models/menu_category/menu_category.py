from app.core.database import Base
from sqlalchemy import Column, Integer, Text, DateTime

class MenuCategory(Base):
    __tablename__ = "menu_category"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False, unique=True)
    title = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)