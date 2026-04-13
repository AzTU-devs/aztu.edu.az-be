from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class InstituteObjective(Base):
    __tablename__ = "institute_objectives"

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="objectives")
    translations = relationship(
        "InstituteObjectiveTr",
        back_populates="objective",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InstituteObjectiveTr(Base):
    __tablename__ = "institute_objective_tr"
    __table_args__ = (
        UniqueConstraint("objective_id", "lang_code", name="uq_institute_objective_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(
        Integer,
        ForeignKey("institute_objectives.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    objective = relationship("InstituteObjective", back_populates="translations")


class InstituteResearchDirection(Base):
    __tablename__ = "institute_research_directions"

    id = Column(Integer, primary_key=True, index=True)
    institute_code = Column(
        String(50),
        ForeignKey("research_institutes.institute_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    institute = relationship("ResearchInstitute", back_populates="research_directions")
    translations = relationship(
        "InstituteResearchDirectionTr",
        back_populates="research_direction",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InstituteResearchDirectionTr(Base):
    __tablename__ = "institute_research_direction_tr"
    __table_args__ = (
        UniqueConstraint("research_direction_id", "lang_code", name="uq_institute_rd_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    research_direction_id = Column(
        Integer,
        ForeignKey("institute_research_directions.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    research_direction = relationship("InstituteResearchDirection", back_populates="translations")
