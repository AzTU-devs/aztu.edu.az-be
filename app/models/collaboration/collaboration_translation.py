from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean

class CollaborationTranslation(Base):
    __tablename__ = "collaboration_translation"

    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, nullable=False, unique=True)
    title = Column(Text, nullable=False)
    lang_code = Column(String(2), nullable=False)