from app.core.database import Base
from sqlalchemy import Column, Integer, Text, String

class MenuTranslation(Base):
    __tablename__ = "menu_translation"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)