from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class TranslationBase(BaseModel):
    lang_code: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InstituteTranslation(BaseModel):
    name: str = Field(...)
    about: str | None = None
    vision: str | None = None
    mission: str | None = None


class InstituteObjectiveTranslation(BaseModel):
    content: str = Field(...)


class InstituteResearchDirectionTranslation(BaseModel):
    content: str = Field(...)


class DirectorTranslation(BaseModel):
    title: str | None = None
    biography: str | None = None


class DirectorEducationTranslation(BaseModel):
    university: str = Field(...)
    degree: str = Field(...)


class DirectorEducationSchema(BaseModel):
    az: DirectorEducationTranslation
    en: DirectorEducationTranslation
    start_year: str | None = None
    end_year: str | None = None
    display_order: int = 0


class DirectorResearchAreaTranslation(BaseModel):
    content: str = Field(...)


class StaffTranslation(BaseModel):
    title: str | None = None


class InstituteObjectiveSchema(BaseModel):
    az: InstituteObjectiveTranslation
    en: InstituteObjectiveTranslation
    display_order: int = 0


class InstituteResearchDirectionSchema(BaseModel):
    az: InstituteResearchDirectionTranslation
    en: InstituteResearchDirectionTranslation
    display_order: int = 0


class DirectorResearchAreaSchema(BaseModel):
    az: DirectorResearchAreaTranslation
    en: DirectorResearchAreaTranslation
    display_order: int = 0


class InstituteDirectorSchema(BaseModel):
    full_name: str = Field(...)
    email: EmailStr | None = None
    office: str | None = None
    image_url: str | None = None
    az: DirectorTranslation
    en: DirectorTranslation
    research_areas: list[DirectorResearchAreaSchema] | None = None
    educations: list[DirectorEducationSchema] | None = None


class InstituteStaffSchema(BaseModel):
    full_name: str = Field(...)
    email: EmailStr | None = None
    phone: str | None = None
    image_url: str | None = None
    display_order: int = 0
    az: StaffTranslation
    en: StaffTranslation


class CreateResearchInstitute(BaseModel):
    institute_code: str = Field(...)
    image_url: str | None = None
    az: InstituteTranslation
    en: InstituteTranslation
    director: InstituteDirectorSchema | None = None
    objectives: list[InstituteObjectiveSchema] | None = None
    research_directions: list[InstituteResearchDirectionSchema] | None = None
    staff: list[InstituteStaffSchema] | None = None


class UpdateResearchInstitute(BaseModel):
    image_url: str | None = None
    az: InstituteTranslation | None = None
    en: InstituteTranslation | None = None
    director: InstituteDirectorSchema | None = None
    objectives: list[InstituteObjectiveSchema] | None = None
    research_directions: list[InstituteResearchDirectionSchema] | None = None
    staff: list[InstituteStaffSchema] | None = None


class ResearchInstituteResponse(BaseModel):
    id: int
    institute_code: str
    image_url: str | None = None
    name: str
    about: str | None = None
    vision: str | None = None
    mission: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
