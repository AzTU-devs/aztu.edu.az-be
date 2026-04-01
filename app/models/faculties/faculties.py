from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedras = relationship(
        "Cafedra",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    director = relationship(
        "FacultyDirector",
        back_populates="faculty",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    laboratories = relationship(
        "FacultyLaboratory",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    research_works = relationship(
        "FacultyResearchWork",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    partner_companies = relationship(
        "FacultyPartnerCompany",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    objectives = relationship(
        "FacultyObjective",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    duties = relationship(
        "FacultyDuty",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    projects = relationship(
        "FacultyProject",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    deputy_deans = relationship(
        "FacultyDeputyDean",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    scientific_council = relationship(
        "FacultyCouncilMember",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    workers = relationship(
        "FacultyWorker",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
