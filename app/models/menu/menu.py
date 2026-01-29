from app.core.database import Base
from sqlalchemy import Column, Integer, Text, DateTime, Boolean

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, nullable=False, unique=True)
    category_id = Column(Integer, nullable=False)
    url = Column(Text)
    display_order = Column(Integer)
    created_at = Column(DateTime, nullable=False)