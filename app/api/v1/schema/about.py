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

from app.api.v1.schema.common import OptionalEmail, OptionalStr, OptionalUrl


class AboutPageTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None
    links_title: OptionalStr = None
    document_label: OptionalStr = None
    pillars_title: OptionalStr = None
    domains: OptionalStr = None
    section_title: OptionalStr = None
    section_body: OptionalStr = None
    # Scientific-board page: the heading above the councils list.
    councils_title: OptionalStr = None
    # Rector page: the academic degree, the title, the message and the bio.
    degree: OptionalStr = None
    position: OptionalStr = None
    message: OptionalStr = None
    about: OptionalStr = None


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


class AboutImagePayload(BaseModel):
    # A pasted URL or the path returned by the image upload endpoint.
    image_url: OptionalUrl = None


class AboutPersonTranslation(BaseModel):
    name: OptionalStr = None
    # Former-rectors page and a partner institution's director.
    surname: OptionalStr = None
    degree: OptionalStr = None
    position: OptionalStr = None
    bio: OptionalStr = None


class AboutPersonPayload(BaseModel):
    email: OptionalEmail = None
    phone: OptionalStr = None
    phone_code: OptionalStr = None
    image_url: OptionalStr = None
    # Former-rectors page: the years the person held office.
    year_start: OptionalStr = None
    year_end: OptionalStr = None
    az: Optional[AboutPersonTranslation] = None
    en: Optional[AboutPersonTranslation] = None


class AboutCouncilMemberTranslation(BaseModel):
    name: OptionalStr = None
    surname: OptionalStr = None
    position: OptionalStr = None


class AboutCouncilMemberPayload(BaseModel):
    az: Optional[AboutCouncilMemberTranslation] = None
    en: Optional[AboutCouncilMemberTranslation] = None


class AboutCouncilTranslation(BaseModel):
    name: OptionalStr = None


class AboutCouncilPayload(BaseModel):
    az: Optional[AboutCouncilTranslation] = None
    en: Optional[AboutCouncilTranslation] = None
    # The council roster and its secretariat, each sent whole and ordered.
    members: Optional[List[AboutCouncilMemberPayload]] = None
    secretaries: Optional[List[AboutCouncilMemberPayload]] = None


class AboutDocCategoryTranslation(BaseModel):
    name: OptionalStr = None


class AboutDocCategoryPayload(BaseModel):
    # Stable, page-local key a document references. Assigned in the dashboard.
    category_key: OptionalStr = None
    az: Optional[AboutDocCategoryTranslation] = None
    en: Optional[AboutDocCategoryTranslation] = None


class AboutDocumentTranslation(BaseModel):
    name: OptionalStr = None


class AboutDocumentPayload(BaseModel):
    # Which category this document belongs to (a category_key), or blank.
    category_key: OptionalStr = None
    # An uploaded file's path or a pasted URL — any format.
    file_url: OptionalStr = None
    az: Optional[AboutDocumentTranslation] = None
    en: Optional[AboutDocumentTranslation] = None


class AboutGradeRow(BaseModel):
    """One row of a Students page's grade-scale table."""

    points: OptionalStr = None
    grade: OptionalStr = None
    description_az: OptionalStr = None
    description_en: OptionalStr = None


class UpdateAboutPage(BaseModel):
    slug_az: OptionalStr = None
    slug_en: OptionalStr = None
    # Either a pasted URL or the path returned by the upload endpoint.
    document_url: OptionalUrl = None

    # Rector page, language-neutral: kept on the page, not per translation.
    experience: OptionalStr = None
    email: OptionalEmail = None
    # The portrait — a pasted URL or the path returned by the image upload.
    image_url: OptionalUrl = None
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
    persons: Optional[List[AboutPersonPayload]] = None
    # The scientific-board councils — each with its members and secretariat.
    councils: Optional[List[AboutCouncilPayload]] = None
    # Regulatory-documents page: the categories and the document cards.
    doc_categories: Optional[List[AboutDocCategoryPayload]] = None
    documents: Optional[List[AboutDocumentPayload]] = None
    # Students pages: the grade-scale table, sent whole.
    grade_scale: Optional[List[AboutGradeRow]] = None
    # The gallery strip — sent whole and replaces what is stored.
    images: Optional[List[AboutImagePayload]] = None

    class Config:
        extra = "ignore"


class PublishAboutPage(BaseModel):
    is_active: bool
