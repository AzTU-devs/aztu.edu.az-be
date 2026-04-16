from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship


class CafedraLaboratory(Base):
    __tablename__ = "cafedra_laboratories"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    image_url = Column(String(1024))
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="laboratories")
    translations = relationship(
        "CafedraLaboratoryTr",
        back_populates="laboratory",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraLaboratoryTr(Base):
    __tablename__ = "cafedra_laboratory_tr"
    __table_args__ = (
        UniqueConstraint("laboratory_id", "lang_code", name="uq_cafedra_laboratory_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    laboratory_id = Column(
        Integer,
        ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    laboratory = relationship("CafedraLaboratory", back_populates="translations")


class CafedraResearchWork(Base):
    __tablename__ = "cafedra_research_works"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="research_works")
    translations = relationship(
        "CafedraResearchWorkTr",
        back_populates="research_work",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraResearchWorkTr(Base):
    __tablename__ = "cafedra_research_work_tr"
    __table_args__ = (
        UniqueConstraint("research_work_id", "lang_code", name="uq_cafedra_research_work_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    research_work_id = Column(
        Integer,
        ForeignKey("cafedra_research_works.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    research_work = relationship("CafedraResearchWork", back_populates="translations")


class CafedraPartnerCompany(Base):
    __tablename__ = "cafedra_partner_companies"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="partner_companies")
    translations = relationship(
        "CafedraPartnerCompanyTr",
        back_populates="partner_company",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraPartnerCompanyTr(Base):
    __tablename__ = "cafedra_partner_company_tr"
    __table_args__ = (
        UniqueConstraint("partner_company_id", "lang_code", name="uq_cafedra_partner_company_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    partner_company_id = Column(
        Integer,
        ForeignKey("cafedra_partner_companies.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    partner_company = relationship("CafedraPartnerCompany", back_populates="translations")


class CafedraObjective(Base):
    __tablename__ = "cafedra_objectives"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="objectives")
    translations = relationship(
        "CafedraObjectiveTr",
        back_populates="objective",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraObjectiveTr(Base):
    __tablename__ = "cafedra_objective_tr"
    __table_args__ = (
        UniqueConstraint("objective_id", "lang_code", name="uq_cafedra_objective_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(
        Integer,
        ForeignKey("cafedra_objectives.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    objective = relationship("CafedraObjective", back_populates="translations")


class CafedraDuty(Base):
    __tablename__ = "cafedra_duties"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="duties")
    translations = relationship(
        "CafedraDutyTr",
        back_populates="duty",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDutyTr(Base):
    __tablename__ = "cafedra_duty_tr"
    __table_args__ = (
        UniqueConstraint("duty_id", "lang_code", name="uq_cafedra_duty_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    duty_id = Column(
        Integer,
        ForeignKey("cafedra_duties.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    duty = relationship("CafedraDuty", back_populates="translations")


class CafedraProject(Base):
    __tablename__ = "cafedra_projects"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="projects")
    translations = relationship(
        "CafedraProjectTr",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraProjectTr(Base):
    __tablename__ = "cafedra_project_tr"
    __table_args__ = (
        UniqueConstraint("project_id", "lang_code", name="uq_cafedra_project_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("cafedra_projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    project = relationship("CafedraProject", back_populates="translations")


class CafedraDirectionOfAction(Base):
    __tablename__ = "cafedra_directions_of_action"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="directions_of_action")
    translations = relationship(
        "CafedraDirectionOfActionTr",
        back_populates="direction_of_action",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraDirectionOfActionTr(Base):
    __tablename__ = "cafedra_direction_of_action_tr"
    __table_args__ = (
        UniqueConstraint("direction_of_action_id", "lang_code", name="uq_cafedra_doa_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    direction_of_action_id = Column(
        Integer,
        ForeignKey("cafedra_directions_of_action.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    direction_of_action = relationship("CafedraDirectionOfAction", back_populates="translations")
