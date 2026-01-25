from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, Integer, String


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    cafedras = relationship(
        "Cafedra",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
