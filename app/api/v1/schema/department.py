from pydantic import BaseModel, EmailStr, Field

from app.api.v1.schema.common import OptionalEmail, OptionalStr


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
    first_name: OptionalStr = None
    last_name: OptionalStr = None
    scientific_degree: str | None = None
    scientific_title: str | None = None
    room: OptionalStr = None
    bio: str | None = None


class DepartmentDirectorPayload(BaseModel):
    first_name: OptionalStr = None
    last_name: OptionalStr = None
    email: OptionalEmail = None
    phone: OptionalStr = None
    phone_code: OptionalStr = None
    profile_image: str | None = None
    az: DirectorTranslation | None = None
    en: DirectorTranslation | None = None
    working_hours: list[DirectorWorkingHour] | None = None
    educations: list[DirectorEducation] | None = None


class WorkerTranslation(BaseModel):
    first_name: OptionalStr = None
    last_name: OptionalStr = None
    duty: str = Field(...)
    scientific_degree: str | None = None
    scientific_name: str | None = None
    room: OptionalStr = None
    working_hours: OptionalStr = None


class DepartmentWorkerPayload(BaseModel):
    first_name: OptionalStr = None
    last_name: OptionalStr = None
    email: OptionalEmail = None
    phone: str | None = None
    phone_code: OptionalStr = None
    profile_image: str | None = None
    az: WorkerTranslation
    en: WorkerTranslation


class WorkerTranslationUpdate(BaseModel):
    first_name: OptionalStr = None
    last_name: OptionalStr = None
    duty: str | None = None
    scientific_degree: str | None = None
    scientific_name: str | None = None
    room: OptionalStr = None
    working_hours: OptionalStr = None


class UpdateDepartmentWorker(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: OptionalEmail = None
    phone: str | None = None
    phone_code: OptionalStr = None
    az: WorkerTranslationUpdate | None = None
    en: WorkerTranslationUpdate | None = None

    class Config:
        extra = "ignore"


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
