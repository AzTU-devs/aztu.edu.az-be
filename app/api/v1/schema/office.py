"""Request bodies for Offices & Centres.

An office is created from just its name (which mints the az/en slugs) and then
saved as one whole document — hero, About, goals, core functions, the director
with an education history, staff and contact details in a single PUT, the way
the About pages save. Publishing is its own call so a draft can never go live by
saving.

Optional text uses ``OptionalStr`` because the admin forms submit "" for blanks.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.api.v1.schema.common import OptionalEmail, OptionalStr


class OfficeCreate(BaseModel):
    """Just the names — the service derives the slugs from them."""

    name_az: OptionalStr = None
    name_en: OptionalStr = None


class OfficeTranslation(BaseModel):
    name: OptionalStr = None
    short_description: OptionalStr = None
    about_title: OptionalStr = None
    about_text: OptionalStr = None
    goal_title: OptionalStr = None
    # One-line goal strings, in order.
    goals: Optional[List[str]] = None
    functions_title: OptionalStr = None
    # Director.
    director_title: OptionalStr = None
    director_name: OptionalStr = None
    director_surname: OptionalStr = None
    director_position: OptionalStr = None
    director_bio: OptionalStr = None
    director_room: OptionalStr = None
    director_work_hours: OptionalStr = None
    # Staff heading.
    staff_title: OptionalStr = None
    # Office contact, per language.
    contact_room: OptionalStr = None
    contact_work_hours: OptionalStr = None


class OfficeFunctionTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None


class OfficeFunctionPayload(BaseModel):
    az: Optional[OfficeFunctionTranslation] = None
    en: Optional[OfficeFunctionTranslation] = None


class OfficeEducationTranslation(BaseModel):
    degree: OptionalStr = None
    university: OptionalStr = None


class OfficeEducationPayload(BaseModel):
    # Free text; end_year is left blank while a degree is still in progress.
    start_year: OptionalStr = None
    end_year: OptionalStr = None
    az: Optional[OfficeEducationTranslation] = None
    en: Optional[OfficeEducationTranslation] = None


class OfficeStaffTranslation(BaseModel):
    name: OptionalStr = None
    surname: OptionalStr = None
    duty: OptionalStr = None


class OfficeStaffPayload(BaseModel):
    phone: OptionalStr = None
    phone_code: OptionalStr = None
    email: OptionalEmail = None
    # A pasted URL or the path returned by the image upload endpoint.
    image_url: OptionalStr = None
    az: Optional[OfficeStaffTranslation] = None
    en: Optional[OfficeStaffTranslation] = None


class UpdateOffice(BaseModel):
    # Language-neutral contact facts.
    director_phone: OptionalStr = None
    director_phone_code: OptionalStr = None
    director_email: OptionalEmail = None
    director_image_url: OptionalStr = None
    contact_phone: OptionalStr = None
    contact_phone_code: OptionalStr = None
    contact_email: OptionalEmail = None
    # `is_active` is deliberately absent: publishing is its own endpoint.

    az: Optional[OfficeTranslation] = None
    en: Optional[OfficeTranslation] = None

    # Omit a key to leave those rows untouched; send [] to clear them.
    functions: Optional[List[OfficeFunctionPayload]] = None
    educations: Optional[List[OfficeEducationPayload]] = None
    staff: Optional[List[OfficeStaffPayload]] = None

    class Config:
        extra = "ignore"


class PublishOffice(BaseModel):
    is_active: bool
