from pydantic import BaseModel, EmailStr, Field


class InstituteTranslation(BaseModel):
    name: str = Field(...)
    about_html: str | None = None
    vision_html: str | None = None
    mission_html: str | None = None
    goals_html: str | None = None
    direction_html: str | None = None


class EducationTranslation(BaseModel):
    degree: str = Field(...)


class DirectorEducation(BaseModel):
    university_name: str = Field(...)
    start_year: str | None = None
    end_year: str | None = None
    az: EducationTranslation
    en: EducationTranslation


class DirectorTranslation(BaseModel):
    scientific_name: str | None = None
    scientific_degree: str | None = None
    bio: str | None = None
    researcher_areas: str | None = None  # Comma separated or text


class InstituteDirectorPayload(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    email: EmailStr | None = None
    room_number: str | None = None
    image: str | None = None
    az: DirectorTranslation
    en: DirectorTranslation
    educations: list[DirectorEducation] | None = None


class StaffTranslation(BaseModel):
    scientific_name: str | None = None
    scientific_degree: str | None = None


class InstituteStaffPayload(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    image: str | None = None
    az: StaffTranslation
    en: StaffTranslation


class CreateResearchInstitute(BaseModel):
    image: str | None = None
    az: InstituteTranslation
    en: InstituteTranslation
    director: InstituteDirectorPayload | None = None
    staff: list[InstituteStaffPayload] | None = None


class UpdateResearchInstitute(BaseModel):
    image: str | None = None
    az: InstituteTranslation | None = None
    en: InstituteTranslation | None = None
    director: InstituteDirectorPayload | None = None
    staff: list[InstituteStaffPayload] | None = None

    class Config:
        extra = "ignore"
