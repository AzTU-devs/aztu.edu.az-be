from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, nullable=False)
    image = Column(String(1024))
    project_url = Column(String(2048))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    translations = relationship(
        "ResearchProjectTr",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    members = relationship(
        "ResearchProjectMember",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ResearchProjectTr(Base):
    __tablename__ = "research_projects_tr"
    __table_args__ = (
        UniqueConstraint("project_code", "lang_code", name="uq_research_projects_tr_code_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(
        String(50),
        ForeignKey("research_projects.project_code", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    name = Column(Text, nullable=False)
    # Free text rather than an enum: the supplied projects range from a two-word
    # label ("Elmi tədqiqat") to a full descriptive paragraph.
    project_type = Column(Text)
    duration = Column(String(255))
    leader_name = Column(String(255))
    # Text, not numeric — real values include "800000", "250 min manat" and "yox".
    budget = Column(String(255))
    about_html = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    project = relationship("ResearchProject", back_populates="translations")


class ResearchProjectMember(Base):
    """A team member. Deliberately not translated — these are personal names,
    and asking an editor to retype the same roster per language earns nothing.
    """

    __tablename__ = "research_project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(
        String(50),
        ForeignKey("research_projects.project_code", ondelete="CASCADE"),
        nullable=False,
    )
    full_name = Column(String(255), nullable=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    project = relationship("ResearchProject", back_populates="members")
