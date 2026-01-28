from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Text,
    DateTime,
    func
)
from app.core.database import Base
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, unique=True, nullable=False)
    bg_image = Column(Text, nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    translations = relationship("ProjectTranslation", back_populates="project", cascade="all, delete")