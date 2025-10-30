from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectTranslationBase(BaseModel):
    lang_code: str
    title: str
    desc: str

class ProjectTranslationCreate(ProjectTranslationBase):
    pass

class ProjectTranslationRead(ProjectTranslationBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    bg_image: str
    is_active: Optional[bool] = False

class ProjectCreate(ProjectBase):
    translations: List[ProjectTranslationCreate]

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
