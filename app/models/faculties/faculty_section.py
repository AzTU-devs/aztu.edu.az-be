from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class FacultyLaboratory(Base):
    __tablename__ = "faculty_laboratories"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="laboratories")
    translations = relationship(
        "FacultyLaboratoryTr",
        back_populates="laboratory",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyLaboratoryTr(Base):
    __tablename__ = "faculty_laboratory_tr"
    __table_args__ = (
        UniqueConstraint("laboratory_id", "lang_code", name="uq_faculty_laboratory_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    laboratory_id = Column(
        Integer,
        ForeignKey("faculty_laboratories.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    laboratory = relationship("FacultyLaboratory", back_populates="translations")


class FacultyResearchWork(Base):
    __tablename__ = "faculty_research_works"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="research_works")
    translations = relationship(
        "FacultyResearchWorkTr",
        back_populates="research_work",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyResearchWorkTr(Base):
    __tablename__ = "faculty_research_work_tr"
    __table_args__ = (
        UniqueConstraint("research_work_id", "lang_code", name="uq_faculty_research_work_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    research_work_id = Column(
        Integer,
        ForeignKey("faculty_research_works.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    research_work = relationship("FacultyResearchWork", back_populates="translations")


class FacultyPartnerCompany(Base):
    __tablename__ = "faculty_partner_companies"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="partner_companies")
    translations = relationship(
        "FacultyPartnerCompanyTr",
        back_populates="partner_company",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyPartnerCompanyTr(Base):
    __tablename__ = "faculty_partner_company_tr"
    __table_args__ = (
        UniqueConstraint("partner_company_id", "lang_code", name="uq_faculty_partner_company_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    partner_company_id = Column(
        Integer,
        ForeignKey("faculty_partner_companies.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    partner_company = relationship("FacultyPartnerCompany", back_populates="translations")


class FacultyObjective(Base):
    __tablename__ = "faculty_objectives"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="objectives")
    translations = relationship(
        "FacultyObjectiveTr",
        back_populates="objective",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyObjectiveTr(Base):
    __tablename__ = "faculty_objective_tr"
    __table_args__ = (
        UniqueConstraint("objective_id", "lang_code", name="uq_faculty_objective_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(
        Integer,
        ForeignKey("faculty_objectives.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    objective = relationship("FacultyObjective", back_populates="translations")


class FacultyDuty(Base):
    __tablename__ = "faculty_duties"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="duties")
    translations = relationship(
        "FacultyDutyTr",
        back_populates="duty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDutyTr(Base):
    __tablename__ = "faculty_duty_tr"
    __table_args__ = (
        UniqueConstraint("duty_id", "lang_code", name="uq_faculty_duty_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    duty_id = Column(
        Integer,
        ForeignKey("faculty_duties.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    duty = relationship("FacultyDuty", back_populates="translations")


class FacultyProject(Base):
    __tablename__ = "faculty_projects"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="projects")
    translations = relationship(
        "FacultyProjectTr",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyProjectTr(Base):
    __tablename__ = "faculty_project_tr"
    __table_args__ = (
        UniqueConstraint("project_id", "lang_code", name="uq_faculty_project_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("faculty_projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    project = relationship("FacultyProject", back_populates="translations")


class FacultyDirectionOfAction(Base):
    __tablename__ = "faculty_directions_of_action"

    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(
        String(50),
        ForeignKey("faculties.faculty_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    faculty = relationship("Faculty", back_populates="directions_of_action")
    translations = relationship(
        "FacultyDirectionOfActionTr",
        back_populates="direction_of_action",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FacultyDirectionOfActionTr(Base):
    __tablename__ = "faculty_direction_of_action_tr"
    __table_args__ = (
        UniqueConstraint(
            "direction_of_action_id",
            "lang_code",
            name="uq_faculty_direction_of_action_tr_id_lang",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    direction_of_action_id = Column(
        Integer,
        ForeignKey("faculty_directions_of_action.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    direction_of_action = relationship(
        "FacultyDirectionOfAction",
        back_populates="translations",
    )
