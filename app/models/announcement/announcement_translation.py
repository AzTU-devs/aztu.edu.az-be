from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    func,
    String
)
from app.core.database import Base

class AnnouncementTranslation(Base):
    __tablename__ = "announcement_translation"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)
    html_content = Column(Text, nullable=False)