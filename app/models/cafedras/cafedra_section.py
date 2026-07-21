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
    room_number = Column(String(50))
    authorized_person = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(50))
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
    objectives = relationship(
        "CafedraLaboratoryObjective",
        back_populates="laboratory",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    equipments = relationship(
        "CafedraLaboratoryEquipment",
        back_populates="laboratory",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    gallery_images = relationship(
        "CafedraLaboratoryGalleryImage",
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


class CafedraLaboratoryObjective(Base):
    __tablename__ = "cafedra_laboratory_objectives"

    id = Column(Integer, primary_key=True, index=True)
    laboratory_id = Column(
        Integer,
        ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    laboratory = relationship("CafedraLaboratory", back_populates="objectives")
    translations = relationship(
        "CafedraLaboratoryObjectiveTr",
        back_populates="objective",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraLaboratoryObjectiveTr(Base):
    __tablename__ = "cafedra_laboratory_objective_tr"
    __table_args__ = (
        UniqueConstraint("objective_id", "lang_code", name="uq_cafedra_lab_objective_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(
        Integer,
        ForeignKey("cafedra_laboratory_objectives.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    objective = relationship("CafedraLaboratoryObjective", back_populates="translations")


class CafedraLaboratoryEquipment(Base):
    __tablename__ = "cafedra_laboratory_equipments"

    id = Column(Integer, primary_key=True, index=True)
    laboratory_id = Column(
        Integer,
        ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"),
        nullable=False,
    )
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    laboratory = relationship("CafedraLaboratory", back_populates="equipments")
    translations = relationship(
        "CafedraLaboratoryEquipmentTr",
        back_populates="equipment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraLaboratoryEquipmentTr(Base):
    __tablename__ = "cafedra_laboratory_equipment_tr"
    __table_args__ = (
        UniqueConstraint("equipment_id", "lang_code", name="uq_cafedra_lab_equipment_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(
        Integer,
        ForeignKey("cafedra_laboratory_equipments.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    name = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    equipment = relationship("CafedraLaboratoryEquipment", back_populates="translations")


class CafedraLaboratoryGalleryImage(Base):
    __tablename__ = "cafedra_laboratory_gallery_images"

    id = Column(Integer, primary_key=True, index=True)
    laboratory_id = Column(
        Integer,
        ForeignKey("cafedra_laboratories.id", ondelete="CASCADE"),
        nullable=False,
    )
    image_url = Column(String(1024), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    laboratory = relationship("CafedraLaboratory", back_populates="gallery_images")


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
    logo_url = Column(String(1024))
    website_url = Column(String(1024))
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
    url = Column(String(1024))
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


class CafedraScientificPublication(Base):
    __tablename__ = "cafedra_scientific_publications"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    publication_index = Column(String(50), nullable=False)
    quartile = Column(String(5))
    published_at = Column(String(50))
    year = Column(Integer, index=True)
    url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="scientific_publications")
    translations = relationship(
        "CafedraScientificPublicationTr",
        back_populates="publication",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraScientificPublicationTr(Base):
    __tablename__ = "cafedra_scientific_publication_tr"
    __table_args__ = (
        UniqueConstraint("publication_id", "lang_code", name="uq_cafedra_scientific_publication_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    publication_id = Column(
        Integer,
        ForeignKey("cafedra_scientific_publications.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(1000), nullable=False)
    authors = Column(Text)
    journal = Column(Text)
    country = Column(String(255))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    publication = relationship("CafedraScientificPublication", back_populates="translations")


class CafedraPatent(Base):
    __tablename__ = "cafedra_patents"

    id = Column(Integer, primary_key=True, index=True)
    cafedra_code = Column(
        String(50),
        ForeignKey("cafedras.cafedra_code", ondelete="CASCADE"),
        nullable=False,
    )
    # Free text: real numbers take several shapes ("İ 2024 0058", "№053029").
    patent_number = Column(String(100))
    year = Column(Integer, index=True)
    url = Column(String(2048))
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    cafedra = relationship("Cafedra", back_populates="patents")
    translations = relationship(
        "CafedraPatentTr",
        back_populates="patent",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class CafedraPatentTr(Base):
    __tablename__ = "cafedra_patent_tr"
    __table_args__ = (
        UniqueConstraint("patent_id", "lang_code", name="uq_cafedra_patent_tr_id_lang"),
    )

    id = Column(Integer, primary_key=True, index=True)
    patent_id = Column(
        Integer,
        ForeignKey("cafedra_patents.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang_code = Column(String(10), nullable=False)
    title = Column(String(1000), nullable=False)
    authors = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True))

    patent = relationship("CafedraPatent", back_populates="translations")
