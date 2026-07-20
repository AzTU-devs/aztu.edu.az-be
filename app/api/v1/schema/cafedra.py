from typing import Annotated, Literal, Optional

from pydantic import BaseModel, BeforeValidator, EmailStr, Field, field_validator

from app.api.v1.schema.common import (
    OptionalEmail,
    OptionalInt,
    OptionalStr,
    OptionalUrl,
    blank_to_none,
)


class LanguageBlock(BaseModel):
    title: str = Field(...)
    html_content: str | None = None


class WorkingHourTranslation(BaseModel):
    day: str = Field(...)


class DirectorWorkingHour(BaseModel):
    az: WorkingHourTranslation
    en: WorkingHourTranslation
    time_range: str = Field(...)


class ScientificEventTranslation(BaseModel):
    event_title: str = Field(...)
    event_description: str | None = None


class DirectorScientificEvent(BaseModel):
    az: ScientificEventTranslation
    en: ScientificEventTranslation


class EducationTranslation(BaseModel):
    degree: str = Field(...)
    university: str = Field(...)


class DirectorEducation(BaseModel):
    az: EducationTranslation
    en: EducationTranslation
    start_year: str | None = None
    end_year: str | None = None


class DirectorTranslation(BaseModel):
    scientific_degree: str | None = None
    scientific_title: str | None = None
    bio: str | None = None
    scientific_research_fields: list[str] | None = None


class CafedraDirectorPayload(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    father_name: str | None = None
    az: DirectorTranslation | None = None
    en: DirectorTranslation | None = None
    email: OptionalEmail = None
    phone: str | None = None
    room_number: str | None = None
    profile_image: str | None = None
    working_hours: list[DirectorWorkingHour] | None = None
    scientific_events: list[DirectorScientificEvent] | None = None
    educations: list[DirectorEducation] | None = None


class SectionTranslation(BaseModel):
    title: str = Field(...)
    description: str | None = None


class SectionItem(BaseModel):
    az: SectionTranslation
    en: SectionTranslation


class LaboratoryObjectiveTranslation(BaseModel):
    title: str = Field(...)


class LaboratoryObjectiveItem(BaseModel):
    az: LaboratoryObjectiveTranslation
    en: LaboratoryObjectiveTranslation


class LaboratoryEquipmentTranslation(BaseModel):
    name: str = Field(...)


class LaboratoryEquipmentItem(BaseModel):
    az: LaboratoryEquipmentTranslation
    en: LaboratoryEquipmentTranslation


class LaboratoryTranslation(BaseModel):
    title: str = Field(...)
    html_content: str | None = None


class LaboratoryItem(BaseModel):
    az: LaboratoryTranslation
    en: LaboratoryTranslation
    room_number: str | None = None
    authorized_person: str | None = None
    email: OptionalEmail = None
    phone_number: str | None = None
    image_url: str | None = None
    objectives: list[LaboratoryObjectiveItem] | None = None
    equipments: list[LaboratoryEquipmentItem] | None = None
    gallery_images: list[str] | None = None


class DeputyDirectorTranslation(BaseModel):
    scientific_name: str | None = None
    scientific_degree: str | None = None
    duty: str | None = None


class DeputyDirector(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    az: DeputyDirectorTranslation | None = None
    en: DeputyDirectorTranslation | None = None
    email: OptionalEmail = None
    phone: str | None = None
    profile_image: str | None = None


class CouncilMemberTranslation(BaseModel):
    duty: str = Field(...)
    scientific_name: str | None = None
    scientific_degree: str | None = None


class ScientificCouncilMember(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    az: CouncilMemberTranslation
    en: CouncilMemberTranslation
    email: OptionalEmail = None
    phone: str | None = None


class WorkerTranslation(BaseModel):
    duty: str = Field(...)
    scientific_name: str | None = None
    scientific_degree: str | None = None


class Worker(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    az: WorkerTranslation
    en: WorkerTranslation
    email: OptionalEmail = None
    phone: str | None = None
    profile_image: str | None = None


# ── Standalone sub-entity update schemas (all-optional, partial updates) ──────────


class WorkerTranslationUpdate(BaseModel):
    duty: str | None = None
    scientific_name: str | None = None
    scientific_degree: str | None = None


class UpdateWorker(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    father_name: str | None = None
    az: WorkerTranslationUpdate | None = None
    en: WorkerTranslationUpdate | None = None
    email: OptionalEmail = None
    phone: str | None = None

    class Config:
        extra = "ignore"


class UpdateDeputyDirector(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    father_name: str | None = None
    az: DeputyDirectorTranslation | None = None
    en: DeputyDirectorTranslation | None = None
    email: OptionalEmail = None
    phone: str | None = None

    class Config:
        extra = "ignore"


class CouncilMemberTranslationUpdate(BaseModel):
    duty: str | None = None
    scientific_name: str | None = None
    scientific_degree: str | None = None


class UpdateCouncilMember(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    father_name: str | None = None
    az: CouncilMemberTranslationUpdate | None = None
    en: CouncilMemberTranslationUpdate | None = None
    email: OptionalEmail = None
    phone: str | None = None

    class Config:
        extra = "ignore"


class LaboratoryTranslationUpdate(BaseModel):
    title: str | None = None
    html_content: str | None = None


class UpdateLaboratory(BaseModel):
    az: LaboratoryTranslationUpdate | None = None
    en: LaboratoryTranslationUpdate | None = None
    room_number: str | None = None
    authorized_person: str | None = None
    email: OptionalEmail = None
    phone_number: str | None = None
    objectives: list[LaboratoryObjectiveItem] | None = None
    equipments: list[LaboratoryEquipmentItem] | None = None

    class Config:
        extra = "ignore"


class CreateCafedra(BaseModel):
    faculty_code: str = Field(...)
    az: LanguageBlock
    en: LanguageBlock
    director: CafedraDirectorPayload | None = None

    # Statistics
    bachelor_programs_count: int | None = 0
    master_programs_count: int | None = 0
    phd_programs_count: int | None = 0
    international_collaborations_count: int | None = 0
    laboratories_count: int | None = 0
    projects_patents_count: int | None = 0
    industrial_collaborations_count: int | None = 0
    sdgs: list[int] | None = None

    laboratories: list[LaboratoryItem] | None = None
    research_works: list[SectionItem] | None = None
    partner_companies: list[SectionItem] | None = None
    objectives: list[SectionItem] | None = None
    duties: list[SectionItem] | None = None
    projects: list[SectionItem] | None = None
    directions_of_action: list[SectionItem] | None = None
    deputy_directors: list[DeputyDirector] | None = None
    scientific_council: list[ScientificCouncilMember] | None = None
    workers: list[Worker] | None = None


class UpdateCafedra(BaseModel):
    az: LanguageBlock | None = None
    en: LanguageBlock | None = None
    director: CafedraDirectorPayload | None = None

    # Statistics
    bachelor_programs_count: int | None = None
    master_programs_count: int | None = None
    phd_programs_count: int | None = None
    international_collaborations_count: int | None = None
    laboratories_count: int | None = None
    projects_patents_count: int | None = None
    industrial_collaborations_count: int | None = None
    sdgs: list[int] | None = None

    laboratories: list[LaboratoryItem] | None = None
    research_works: list[SectionItem] | None = None
    partner_companies: list[SectionItem] | None = None
    objectives: list[SectionItem] | None = None
    duties: list[SectionItem] | None = None
    projects: list[SectionItem] | None = None
    directions_of_action: list[SectionItem] | None = None
    deputy_directors: list[DeputyDirector] | None = None
    scientific_council: list[ScientificCouncilMember] | None = None
    workers: list[Worker] | None = None

    class Config:
        extra = "ignore"


# ── Scientific activity (elmi fəaliyyət) ─────────────────────────────────────────

PublicationIndex = Literal["Scopus", "Web of Science", "Scopus / Web of Science"]
OptionalQuartile = Annotated[
    Optional[Literal["Q1", "Q2", "Q3", "Q4"]], BeforeValidator(blank_to_none)
]


def _validate_year(value: int | None) -> int | None:
    if value is None:
        return None
    if not (1900 <= value <= 2100):
        raise ValueError("year must be between 1900 and 2100")
    return value


class RichTextTranslation(BaseModel):
    title: str = Field(...)
    html_content: OptionalStr = None


class RichTextSectionItem(BaseModel):
    az: RichTextTranslation
    en: RichTextTranslation

    class Config:
        extra = "ignore"


class ProjectGrantTranslation(BaseModel):
    title: str = Field(...)
    description: OptionalStr = None


class ProjectGrantItem(BaseModel):
    az: ProjectGrantTranslation
    en: ProjectGrantTranslation
    url: OptionalUrl = None

    class Config:
        extra = "ignore"


class PartnerCompanyTranslation(BaseModel):
    title: str = Field(...)
    description: OptionalStr = None


class PartnerCompanyItem(BaseModel):
    az: PartnerCompanyTranslation
    en: PartnerCompanyTranslation
    website_url: OptionalUrl = None

    class Config:
        extra = "ignore"


class PublicationTranslation(BaseModel):
    title: str = Field(..., max_length=1000)
    authors: OptionalStr = None
    journal: OptionalStr = None
    country: OptionalStr = None


class PublicationItem(BaseModel):
    az: PublicationTranslation
    en: PublicationTranslation
    index: PublicationIndex = "Scopus"
    quartile: OptionalQuartile = None
    date: OptionalStr = None
    year: OptionalInt = None
    url: OptionalUrl = None

    class Config:
        extra = "ignore"

    @field_validator("year")
    @classmethod
    def _valid_year(cls, value):
        return _validate_year(value)


class ScientificIntroTranslation(BaseModel):
    research_areas_intro: OptionalStr = None
    projects_grants_intro: OptionalStr = None
    publications_intro: OptionalStr = None
    industry_cooperation_intro: OptionalStr = None
    international_cooperation_intro: OptionalStr = None

    class Config:
        extra = "ignore"


class UpdateScientificIntros(BaseModel):
    az: ScientificIntroTranslation | None = None
    en: ScientificIntroTranslation | None = None

    class Config:
        extra = "ignore"


class ReorderRequest(BaseModel):
    ids: list[int] = Field(default_factory=list)


# ── Scientific activity partial-update mirrors ───────────────────────────────────


class RichTextTranslationUpdate(BaseModel):
    title: str | None = None
    html_content: OptionalStr = None


class UpdateRichTextSectionItem(BaseModel):
    az: RichTextTranslationUpdate | None = None
    en: RichTextTranslationUpdate | None = None

    class Config:
        extra = "ignore"


class ProjectGrantTranslationUpdate(BaseModel):
    title: str | None = None
    description: OptionalStr = None


class UpdateProjectGrantItem(BaseModel):
    az: ProjectGrantTranslationUpdate | None = None
    en: ProjectGrantTranslationUpdate | None = None
    url: OptionalUrl = None

    class Config:
        extra = "ignore"


class PartnerCompanyTranslationUpdate(BaseModel):
    title: str | None = None
    description: OptionalStr = None


class UpdatePartnerCompanyItem(BaseModel):
    az: PartnerCompanyTranslationUpdate | None = None
    en: PartnerCompanyTranslationUpdate | None = None
    website_url: OptionalUrl = None

    class Config:
        extra = "ignore"


class PublicationTranslationUpdate(BaseModel):
    title: Annotated[str, Field(max_length=1000)] | None = None
    authors: OptionalStr = None
    journal: OptionalStr = None
    country: OptionalStr = None


class UpdatePublicationItem(BaseModel):
    az: PublicationTranslationUpdate | None = None
    en: PublicationTranslationUpdate | None = None
    index: PublicationIndex | None = None
    quartile: OptionalQuartile = None
    date: OptionalStr = None
    year: OptionalInt = None
    url: OptionalUrl = None

    class Config:
        extra = "ignore"

    @field_validator("year")
    @classmethod
    def _valid_year(cls, value):
        return _validate_year(value)
