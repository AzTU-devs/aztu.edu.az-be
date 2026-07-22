"""Request bodies for the About-page CMS.

Every translated payload arrives as an ``{az: {...}, en: {...}}`` pair, matching
the shape the other bilingual admin forms already post. Optional text uses
``OptionalStr`` throughout because the dashboard submits "" for anything left
blank, and a bare ``str | None`` would 422 on that.
"""

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from app.api.v1.schema.common import OptionalEmail, OptionalStr, OptionalUrl

# ── Page ───────────────────────────────────────────────────────────────────────


class AboutPageTranslation(BaseModel):
    eyebrow: OptionalStr = None
    title: OptionalStr = None
    subtitle: OptionalStr = None
    breadcrumb: OptionalStr = None
    intro: OptionalStr = None
    meta_title: OptionalStr = None
    meta_description: OptionalStr = None


class UpdateAboutPage(BaseModel):
    """Page-level fields only. Sections are edited through their own endpoints."""

    group_key: OptionalStr = None
    template: OptionalStr = None
    slug_az: OptionalStr = None
    slug_en: OptionalStr = None
    display_order: Optional[int] = None
    # `is_active` is deliberately absent: going live is its own endpoint under
    # its own permission, so a page cannot be published as a side effect of
    # saving a half-written paragraph.

    hero_image: OptionalStr = None
    hero_video_url: OptionalUrl = None
    cover_image: OptionalStr = None
    pdf_url: OptionalUrl = None
    pdf_filename: OptionalStr = None
    website_url: OptionalUrl = None
    video_url: OptionalUrl = None

    az: Optional[AboutPageTranslation] = None
    en: Optional[AboutPageTranslation] = None

    class Config:
        extra = "ignore"


class CreateAboutPage(UpdateAboutPage):
    page_key: str = Field(..., min_length=1, max_length=100)


class PublishAboutPage(BaseModel):
    is_active: bool


# ── Section ────────────────────────────────────────────────────────────────────


class AboutSectionTranslation(BaseModel):
    title: OptionalStr = None
    subtitle: OptionalStr = None
    description: OptionalStr = None
    body_html: OptionalStr = None
    footer: OptionalStr = None
    note: OptionalStr = None
    cta_label: OptionalStr = None
    pdf_url: OptionalUrl = None
    video_url: OptionalUrl = None
    list_intro: OptionalStr = None
    headers: Optional[List[str]] = None


class UpdateAboutSection(BaseModel):
    section_key: OptionalStr = None
    section_type: OptionalStr = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

    image_url: OptionalStr = None
    link_url: OptionalUrl = None
    pdf_url: OptionalUrl = None
    video_url: OptionalUrl = None
    icon: OptionalStr = None
    extra: Optional[Any] = None

    az: Optional[AboutSectionTranslation] = None
    en: Optional[AboutSectionTranslation] = None

    class Config:
        extra = "ignore"


class CreateAboutSection(UpdateAboutSection):
    section_key: str = Field(..., min_length=1, max_length=100)
    section_type: str = Field("paragraphs", min_length=1, max_length=50)


# ── Item ───────────────────────────────────────────────────────────────────────


class AboutItemTranslation(BaseModel):
    title: OptionalStr = None
    subtitle: OptionalStr = None
    description: OptionalStr = None
    label: OptionalStr = None
    value_text: OptionalStr = None
    caption: OptionalStr = None
    link_label: OptionalStr = None
    file_url: OptionalUrl = None
    # Free-form sub-list: ["Əyani: 3 il", ...] or a table row's cells.
    extra: Optional[Any] = None


class UpdateAboutItem(BaseModel):
    display_order: Optional[int] = None
    item_key: OptionalStr = None
    is_active: Optional[bool] = None

    image_url: OptionalStr = None
    link_url: OptionalUrl = None
    pdf_url: OptionalUrl = None
    email: OptionalEmail = None
    phone: OptionalStr = None
    icon: OptionalStr = None
    slug: OptionalStr = None
    year: OptionalStr = None
    num: OptionalStr = None
    value: OptionalStr = None
    extra: Optional[Any] = None

    az: Optional[AboutItemTranslation] = None
    en: Optional[AboutItemTranslation] = None

    class Config:
        extra = "ignore"


class CreateAboutItem(UpdateAboutItem):
    pass


class ReorderPayload(BaseModel):
    """`[{id, display_order}, ...]` — one write per drag, not one per row moved."""

    ids: List[int] = Field(..., min_length=1)


# ── Person ─────────────────────────────────────────────────────────────────────


class AboutPersonEducationTranslation(BaseModel):
    degree: OptionalStr = None
    institution: OptionalStr = None


class AboutPersonEducationPayload(BaseModel):
    period: OptionalStr = None
    display_order: Optional[int] = None
    az: Optional[AboutPersonEducationTranslation] = None
    en: Optional[AboutPersonEducationTranslation] = None


class AboutPersonTranslation(BaseModel):
    full_name: OptionalStr = None
    degree: OptionalStr = None
    position: OptionalStr = None
    office: OptionalStr = None
    hours: OptionalStr = None
    bio_html: OptionalStr = None
    achievements: OptionalStr = None
    research_interests: OptionalStr = None


class UpdateAboutPerson(BaseModel):
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

    slug: OptionalStr = None
    image_url: OptionalStr = None
    email: OptionalEmail = None
    phone: OptionalStr = None
    phone_internal: OptionalStr = None
    room_number: OptionalStr = None

    az: Optional[AboutPersonTranslation] = None
    en: Optional[AboutPersonTranslation] = None
    # Sent whole. Omit the key to leave the existing rows untouched; send [] to
    # clear them.
    educations: Optional[List[AboutPersonEducationPayload]] = None

    class Config:
        extra = "ignore"


class CreateAboutPerson(UpdateAboutPerson):
    pass
