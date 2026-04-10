from pydantic import BaseModel, EmailStr, Field


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
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    az: DirectorTranslation | None = None
    en: DirectorTranslation | None = None
    email: EmailStr | None = None
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
    email: EmailStr | None = None
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
    email: EmailStr | None = None
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
    email: EmailStr | None = None
    phone: str | None = None
    profile_image: str | None = None


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

    laboratories: list[SectionItem] | None = None
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

    laboratories: list[SectionItem] | None = None
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
