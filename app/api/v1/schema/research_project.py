from pydantic import BaseModel, Field

from app.api.v1.schema.common import OptionalStr, OptionalUrl


class ProjectTranslation(BaseModel):
    name: str = Field(...)
    project_type: OptionalStr = None
    duration: OptionalStr = None
    leader_name: OptionalStr = None
    budget: OptionalStr = None
    about_html: str | None = None


class ProjectMemberPayload(BaseModel):
    full_name: str = Field(..., min_length=1)


class CreateResearchProject(BaseModel):
    image: str | None = None
    project_url: OptionalUrl = None
    az: ProjectTranslation
    en: ProjectTranslation
    members: list[ProjectMemberPayload] | None = None


class UpdateResearchProject(BaseModel):
    image: str | None = None
    project_url: OptionalUrl = None
    az: ProjectTranslation | None = None
    en: ProjectTranslation | None = None
    members: list[ProjectMemberPayload] | None = None

    class Config:
        extra = "ignore"
