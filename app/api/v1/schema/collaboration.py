from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, Form


class CollaborationTranslationCreateForm:
    def __init__(
        self,
        name: str = Form(...)
    ):
        self.name = name


class CollaborationCreate:
    def __init__(
        self,
        logo: UploadFile,
        website_url: Optional[str],
        az: CollaborationTranslationCreateForm,
        en: CollaborationTranslationCreateForm
    ):
        self.logo = logo
        self.website_url = website_url
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        logo: UploadFile = Form(...),
        website_url: Optional[str] = Form(None),
        az_name: str = Form(...),
        en_name: str = Form(...)
    ):
        az = CollaborationTranslationCreateForm(name=az_name)
        en = CollaborationTranslationCreateForm(name=en_name)
        return cls(logo=logo, website_url=website_url, az=az, en=en)


class CollaborationUpdate:
    def __init__(
        self,
        logo: Optional[UploadFile],
        website_url: Optional[str],
        az: CollaborationTranslationCreateForm,
        en: CollaborationTranslationCreateForm
    ):
        self.logo = logo
        self.website_url = website_url
        self.az = az
        self.en = en

    @classmethod
    def as_form(
        cls,
        logo: Optional[UploadFile] = Form(None),
        website_url: Optional[str] = Form(None),
        az_name: str = Form(...),
        en_name: str = Form(...)
    ):
        az = CollaborationTranslationCreateForm(name=az_name)
        en = CollaborationTranslationCreateForm(name=en_name)
        return cls(logo=logo, website_url=website_url, az=az, en=en)


class ReOrderCollaboration(BaseModel):
    collaboration_id: int
    new_order: int
