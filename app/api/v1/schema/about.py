"""Request bodies for the About section.

The page is small enough to save as one document — hero copy, cards and buttons
in a single PUT — so there is one write schema rather than a per-row CRUD
surface. `blocks` and `links` are sent whole and replace what is stored, which
is exactly what the dashboard's single Save button does.

Optional text uses ``OptionalStr`` because the admin forms submit "" for
anything left blank, and a bare ``str | None`` would 422 on that.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.api.v1.schema.common import OptionalStr, OptionalUrl


class AboutPageTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None
    links_title: OptionalStr = None
    document_label: OptionalStr = None
    pillars_title: OptionalStr = None


class AboutBlockTranslation(BaseModel):
    title: OptionalStr = None
    body: OptionalStr = None


class AboutBlockPayload(BaseModel):
    block_key: OptionalStr = None
    az: Optional[AboutBlockTranslation] = None
    en: Optional[AboutBlockTranslation] = None


class AboutLinkTranslation(BaseModel):
    label: OptionalStr = None


class AboutLinkPayload(BaseModel):
    url: OptionalUrl = None
    az: Optional[AboutLinkTranslation] = None
    en: Optional[AboutLinkTranslation] = None


class AboutMilestoneTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None


class AboutMilestonePayload(BaseModel):
    # Free text on purpose: the timeline ends on "Bu gün" / "Today", and some
    # entries span a range. The API decides the ordering, not this value's type.
    year: OptionalStr = None
    az: Optional[AboutMilestoneTranslation] = None
    en: Optional[AboutMilestoneTranslation] = None


class AboutPillarTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None
    # Ordered plain strings — the chips under the card.
    tags: Optional[List[str]] = None


class AboutPillarPayload(BaseModel):
    az: Optional[AboutPillarTranslation] = None
    en: Optional[AboutPillarTranslation] = None


class AboutListTranslation(BaseModel):
    title: OptionalStr = None
    items: Optional[List[str]] = None


class AboutListPayload(BaseModel):
    list_key: OptionalStr = None
    style: OptionalStr = None
    az: Optional[AboutListTranslation] = None
    en: Optional[AboutListTranslation] = None


class UpdateAboutPage(BaseModel):
    slug_az: OptionalStr = None
    slug_en: OptionalStr = None
    # Either a pasted URL or the path returned by the upload endpoint.
    document_url: OptionalUrl = None
    # `is_active` is deliberately absent: publishing is its own endpoint under
    # its own permission, so a page cannot go live as a side effect of saving
    # a half-written paragraph.

    az: Optional[AboutPageTranslation] = None
    en: Optional[AboutPageTranslation] = None

    # Omit a key to leave those rows untouched; send [] to clear them.
    blocks: Optional[List[AboutBlockPayload]] = None
    links: Optional[List[AboutLinkPayload]] = None
    milestones: Optional[List[AboutMilestonePayload]] = None
    pillars: Optional[List[AboutPillarPayload]] = None
    lists: Optional[List[AboutListPayload]] = None

    class Config:
        extra = "ignore"


class PublishAboutPage(BaseModel):
    is_active: bool
