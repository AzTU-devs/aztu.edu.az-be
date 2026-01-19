from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, Form, Depends

class ProjectTranslationBase(BaseModel):
    lang_code: str
    title: str
    desc: str
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
        desc: str = Form(...),
        content_html: str = Form(...)
    ):
        self.title = title
        self.desc = desc
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
        az_desc: str = Form(...),
        az_content_html: str = Form(...),
        en_title: str = Form(...),
        en_desc: str = Form(...),
        en_content_html: str = Form(...)
    ):
        az = ProjectTranslationCreateForm(
            title=az_title,
            desc=az_desc,
            content_html=az_content_html
        )
        en = ProjectTranslationCreateForm(
            title=en_title,
            desc=en_desc,
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