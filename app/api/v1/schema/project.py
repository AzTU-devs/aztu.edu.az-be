from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, Form, Depends

class ProjectTranslationBase(BaseModel):
    lang_code: str
    title: str
    description: str
    content_html: str

class ProjectTranslationCreate(ProjectTranslationBase):
    pass

class ProjectTranslationRead(ProjectTranslationBase):
    id: int
    class Config:
        orm_mode = True
    
class ProjectTranslationCreateForm:
    def __init__(
        self,
        title: str = Form(...),
        description: str = Form(...),
        content_html: str = Form(...)
    ):
        self.title = title
        self.description = description
        self.content_html = content_html


class ProjectCreate:
    def __init__(
        self,
        bg_image: UploadFile = Depends(),
        az: ProjectTranslationCreateForm = Depends(),
        en: ProjectTranslationCreateForm = Depends()
    ):
        self.bg_image = bg_image
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        bg_image: UploadFile = Form(...),
        az_title: str = Form(...),
        az_description: str = Form(...),
        az_content_html: str = Form(...),
        en_title: str = Form(...),
        en_description: str = Form(...),
        en_content_html: str = Form(...)
    ):
        az = ProjectTranslationCreateForm(
            title=az_title,
            description=az_description,
            content_html=az_content_html
        )
        en = ProjectTranslationCreateForm(
            title=en_title,
            description=en_description,
            content_html=en_content_html
        )
        return cls(bg_image=bg_image, az=az, en=en)

class ReOrderProject(BaseModel):
    project_id: str
    new_order: int

class ProjectBase(BaseModel):
    bg_image: str
    is_active: Optional[bool] = False

class ProjectRead(ProjectBase):
    id: int
    project_id: int
    display_order: int
    created_at: datetime
    updated_at: Optional[datetime]
    translations: List[ProjectTranslationRead]

    class Config:
        orm_mode = True

class ProjectReorder(BaseModel):
    project_id: int
    new_order: int