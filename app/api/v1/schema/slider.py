from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile, Form, Depends, File  # ✅ import File


class SliderTranslationBase(BaseModel):
    lang_code: str
    desc: str


class SliderTranslationRead(SliderTranslationBase):
    id: int

    class Config:
        orm_mode = True


class SliderTranslationCreateForm:
    def __init__(self, desc: str = Form(...)):
        self.desc = desc


class SliderCreate:
    """
    Multipart/form-data input:
      - image: file
      - az_desc: str
      - en_desc: str
      - url: str
    """
    def __init__(
        self,
        image: UploadFile = Depends(),
        az: SliderTranslationCreateForm = Depends(),
        en: SliderTranslationCreateForm = Depends(),
        url: str = Form(...),
    ):
        self.image = image
        self.az = az
        self.en = en
        self.url = url

    @classmethod
    def as_form(
        cls,
        image: UploadFile = File(...),
        az_desc: str = Form(...),
        en_desc: str = Form(...),
        url: str = Form(...),
    ):
        az = SliderTranslationCreateForm(desc=az_desc)
        en = SliderTranslationCreateForm(desc=en_desc)
        return cls(image=image, az=az, en=en, url=url)


class SliderRead(BaseModel):
    id: int
    slider_id: int
    url: str
    image: str
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    translations: List[SliderTranslationRead]

    class Config:
        orm_mode = True


class ReOrderSlider(BaseModel):
    slider_id: int
    new_order: int
