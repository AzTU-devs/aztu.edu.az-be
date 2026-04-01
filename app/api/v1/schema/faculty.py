from pydantic import BaseModel, EmailStr, Field


class LanguageBlock(BaseModel):
    title: str = Field(...)
    html_content: str | None = None


class DirectorWorkingHour(BaseModel):
    day: str = Field(...)
    time_range: str = Field(...)


class DirectorScientificEvent(BaseModel):
    event_title: str = Field(...)
    event_description: str | None = None


class DirectorEducation(BaseModel):
    degree: str = Field(...)
    university: str = Field(...)
    start_year: str | None = None
    end_year: str | None = None


class FacultyDirectorPayload(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    scientific_degree: str | None = None
    scientific_title: str | None = None
    bio: str | None = None
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


class DeputyDean(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    scientific_name: str | None = None
    scientific_degree: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    duty: str | None = None
    profile_image: str | None = None


class ScientificCouncilMember(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    duty: str = Field(...)


class Worker(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    duty: str = Field(...)
    scientific_name: str | None = None
    scientific_degree: str | None = None
    email: EmailStr | None = None


class CreateFaculty(BaseModel):
    az: LanguageBlock
    en: LanguageBlock
    director: FacultyDirectorPayload | None = None
    laboratories: list[SectionItem] | None = None
    research_works: list[SectionItem] | None = None
    partner_companies: list[SectionItem] | None = None
    objectives: list[SectionItem] | None = None
    duties: list[SectionItem] | None = None
    projects: list[SectionItem] | None = None
    deputy_deans: list[DeputyDean] | None = None
    scientific_council: list[ScientificCouncilMember] | None = None
    workers: list[Worker] | None = None


class UpdateFaculty(BaseModel):
    az: LanguageBlock | None = None
    en: LanguageBlock | None = None
    director: FacultyDirectorPayload | None = None
    laboratories: list[SectionItem] | None = None
    research_works: list[SectionItem] | None = None
    partner_companies: list[SectionItem] | None = None
    objectives: list[SectionItem] | None = None
    duties: list[SectionItem] | None = None
    projects: list[SectionItem] | None = None
    deputy_deans: list[DeputyDean] | None = None
    scientific_council: list[ScientificCouncilMember] | None = None
    workers: list[Worker] | None = None

    class Config:
        extra = "ignore"
