from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text

class NewsTranslation(Base):
    __tablename__ = "news_translation"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)
    html_content = Column(Text, nullable=False)