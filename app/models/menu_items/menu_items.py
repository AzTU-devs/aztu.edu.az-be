from app.core.database import Base
from sqlalchemy import Column, Integer, DateTime, Text

class MenuItems(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False, unique=True)
    url = Column(Text, nullable=False)
    display_order = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)