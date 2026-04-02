from pydantic import BaseModel, EmailStr, Field


class DepartmentTranslation(BaseModel):
    department_name: str = Field(...)
    about_html: str | None = None


class HtmlContentTranslation(BaseModel):
    html_content: str = Field(...)


class HtmlContentItem(BaseModel):
    az: HtmlContentTranslation
    en: HtmlContentTranslation


class WorkingHourTranslation(BaseModel):
    day: str = Field(...)


class DirectorWorkingHour(BaseModel):
    time_range: str = Field(...)
    az: WorkingHourTranslation
    en: WorkingHourTranslation


class EducationTranslation(BaseModel):
    degree: str = Field(...)
    university: str = Field(...)


class DirectorEducation(BaseModel):
    start_year: str | None = None
    end_year: str | None = None
    az: EducationTranslation
    en: EducationTranslation


class DirectorTranslation(BaseModel):
    scientific_degree: str | None = None
    scientific_title: str | None = None
    bio: str | None = None


class DepartmentDirectorPayload(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    room_number: str | None = None
    profile_image: str | None = None
    az: DirectorTranslation | None = None
    en: DirectorTranslation | None = None
    working_hours: list[DirectorWorkingHour] | None = None
    educations: list[DirectorEducation] | None = None


class WorkerTranslation(BaseModel):
    duty: str = Field(...)
    scientific_degree: str | None = None
    scientific_name: str | None = None


class DepartmentWorkerPayload(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    father_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    profile_image: str | None = None
    az: WorkerTranslation
    en: WorkerTranslation


class CreateDepartment(BaseModel):
    az: DepartmentTranslation
    en: DepartmentTranslation
    objectives: list[HtmlContentItem] | None = None
    core_functions: list[HtmlContentItem] | None = None
    director: DepartmentDirectorPayload | None = None
    workers: list[DepartmentWorkerPayload] | None = None


class UpdateDepartment(BaseModel):
    az: DepartmentTranslation | None = None
    en: DepartmentTranslation | None = None
    objectives: list[HtmlContentItem] | None = None
    core_functions: list[HtmlContentItem] | None = None
    director: DepartmentDirectorPayload | None = None
    workers: list[DepartmentWorkerPayload] | None = None

    class Config:
        extra = "ignore"
