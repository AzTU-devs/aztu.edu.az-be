from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class ProjectTranslation(Base):
    __tablename__ = "project_translation"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.project_id"), nullable=False)
    lang_code = Column(String(2), nullable=False)
    title = Column(Text, nullable=False)
    desc = Column(Text, nullable=False)

    project = relationship("Project", back_populates="translations")
