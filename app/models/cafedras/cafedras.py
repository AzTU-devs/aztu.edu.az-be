from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, JSON
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

    # Statistics
    bachelor_programs_count = Column(Integer, default=0)
    master_programs_count = Column(Integer, default=0)
    phd_programs_count = Column(Integer, default=0)
    international_collaborations_count = Column(Integer, default=0)
    laboratories_count = Column(Integer, default=0)
    projects_patents_count = Column(Integer, default=0)
    industrial_collaborations_count = Column(Integer, default=0)
    sdgs = Column(JSON, default=list)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="cafedras")
    translations = relationship(
        "CafedraTr",
        back_populates="cafedra",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    director = relationship(
        "CafedraDirector",
        back_populates="cafedra",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    workers = relationship(
        "CafedraWorker",
        back_populates="cafedra",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    directions_of_action = relationship(
        "CafedraDirectionOfAction",
        back_populates="cafedra",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
