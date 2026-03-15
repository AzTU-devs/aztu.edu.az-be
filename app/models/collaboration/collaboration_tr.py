from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class CollaborationTranslation(Base):
    __tablename__ = "collaboration_translation"

    id = Column(Integer, primary_key=True, index=True)
    collaboration_id = Column(Integer, ForeignKey("collaboration.collaboration_id"), nullable=False)
    lang_code = Column(String(2), nullable=False)
    name = Column(String(255), nullable=False)

    collaboration = relationship("Collaboration", back_populates="translations")
