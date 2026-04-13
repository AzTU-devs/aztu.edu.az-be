from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

# Import models to register them for relationships
from app.models.research_institutes.institute_details import InstituteObjective, InstituteResearchDirection
from app.models.research_institutes.institute_people import InstituteDirector, InstituteStaff


class ResearchInstitute(Base):
    __tablename__ = "research_institutes"
    __table_args__ = (
        UniqueConstraint("institute_code", name="uq_research_institutes_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(String(50), nullable=False)
    image_url = Column(String(1024))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "ResearchInstituteTr",
        back_populates="institute",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    objectives = relationship(
        "InstituteObjective",
        back_populates="institute",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    research_directions = relationship(
        "InstituteResearchDirection",
        back_populates="institute",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    director = relationship(
        "InstituteDirector",
        back_populates="institute",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    staff = relationship(
        "InstituteStaff",
        back_populates="institute",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchInstituteTr(Base):
    __tablename__ = "research_institutes_tr"
    __table_args__ = (
        UniqueConstraint("institute_code", "lang_code", name="uq_research_institutes_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    name = Column(String(255), nullable=False)
    about = Column(Text)
    vision = Column(Text)
    mission = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="translations")
