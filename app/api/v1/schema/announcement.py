from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile, Form, Depends

class CreateAnnouncementForm:
    def __init__(
        self,
        title: str = Form(...),
        html_content: str = Form(...)
    ):
        self.title = title
        self.html_content = html_content

class CreateAnnouncement:
    def __init__(
        self,
        image: UploadFile = Depends(),
        az: CreateAnnouncementForm = Depends(),
        en: CreateAnnouncementForm = Depends()
    ):
        self.image = image
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        image: UploadFile = Form(...),
        az_title: str = Form(...),
        az_html_content: str = Form(...),
        en_title: str = Form(...),
        en_html_content: str = Form(...)
    ):
        az = CreateAnnouncementForm(
            title=az_title,
            html_content=az_html_content
        )
        en = CreateAnnouncementForm(
            title=en_title,
            html_content=en_html_content
        )
        return cls(image=image, az=az, en=en)

class ReOrderAnnouncement(BaseModel):
    announcement_id: int
    new_order: int