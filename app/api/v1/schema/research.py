"""Request bodies for the Research section.

Mirrors the About section: the page is small enough to save as one document —
hero copy, the intro text, the cards or patent tables and the buttons in a
single PUT — so there is one write schema rather than a per-row CRUD surface.
`priorities`, `patent_years` and `links` are sent whole and replace what is
stored, which is exactly what the dashboard's single Save button does.

One schema covers every template. A page sends the keys its own shape has and
omits the rest, so the priorities page never mentions `patent_years` and the
patents page never mentions `priorities`.

Optional text uses ``OptionalStr`` because the admin forms submit "" for
anything left blank, and a bare ``str | None`` would 422 on that.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.api.v1.schema.common import OptionalStr, OptionalUrl


class ResearchPageTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None
    body_html: OptionalStr = None
    links_title: OptionalStr = None


class ResearchPriorityTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None


class ResearchPriorityPayload(BaseModel):
    az: Optional[ResearchPriorityTranslation] = None
    en: Optional[ResearchPriorityTranslation] = None


class ResearchPatentTranslation(BaseModel):
    name: OptionalStr = None
    # One line, as the table renders it — free-text credits, not employee links.
    authors: OptionalStr = None


class ResearchPatentPayload(BaseModel):
    patent_number: OptionalStr = None
    # A pasted URL or the path returned by the upload endpoint.
    document_url: OptionalUrl = None
    az: Optional[ResearchPatentTranslation] = None
    en: Optional[ResearchPatentTranslation] = None


class ResearchPatentYearPayload(BaseModel):
    year: OptionalStr = None
    patents: Optional[List[ResearchPatentPayload]] = None


class ResearchLinkTranslation(BaseModel):
    label: OptionalStr = None


class ResearchLinkPayload(BaseModel):
    url: OptionalUrl = None
    az: Optional[ResearchLinkTranslation] = None
    en: Optional[ResearchLinkTranslation] = None


class UpdateResearchPage(BaseModel):
    slug_az: OptionalStr = None
    slug_en: OptionalStr = None
    # `is_active` is deliberately absent: publishing is its own endpoint under
    # its own permission, so a page cannot go live as a side effect of saving
    # a half-written paragraph.

    az: Optional[ResearchPageTranslation] = None
    en: Optional[ResearchPageTranslation] = None

    # Omit a key to leave those rows untouched; send [] to clear them.
    priorities: Optional[List[ResearchPriorityPayload]] = None
    patent_years: Optional[List[ResearchPatentYearPayload]] = None
    links: Optional[List[ResearchLinkPayload]] = None

    class Config:
        extra = "ignore"


class PublishResearchPage(BaseModel):
    is_active: bool
