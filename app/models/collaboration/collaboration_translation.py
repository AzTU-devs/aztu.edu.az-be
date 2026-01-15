from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    String
)
from app.core.database import Base

class CollaborationTranslation(Base):
    __tablename__ = "collaboration_translation"

    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, nullable=False, unique=True)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)
