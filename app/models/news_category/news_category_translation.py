from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean

class NewsCategoryTranslation(Base):
    __tablename__ = "news_category_translation"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)