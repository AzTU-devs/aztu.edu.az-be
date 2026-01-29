from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text

class MenuItemsTranslation(Base):
    __tablename__ = "menu_items_translation"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)