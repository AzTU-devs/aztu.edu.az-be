from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship


class Cafedra(Base):
    __tablename__ = "cafedras"
    __table_args__ = (
        UniqueConstraint("cafedra_code", name="uq_cafedras_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    cafedra_code = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    faculty = relationship("Faculty", back_populates="cafedras")
    translations = relationship(
        "CafedraTr",
        back_populates="cafedra",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
