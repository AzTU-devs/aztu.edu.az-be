"""Request bodies for the Research section.

Mirrors the About section: the page is small enough to save as one document —
hero copy, the strategic-outlook text, the priority cards and the buttons in a
single PUT — so there is one write schema rather than a per-row CRUD surface.
`priorities` and `links` are sent whole and replace what is stored, which is
exactly what the dashboard's single Save button does.

Optional text uses ``OptionalStr`` because the admin forms submit "" for
anything left blank, and a bare ``str | None`` would 422 on that.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.api.v1.schema.common import OptionalStr, OptionalUrl


class ResearchPageTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None
    vision_html: OptionalStr = None
    links_title: OptionalStr = None


class ResearchPriorityTranslation(BaseModel):
    title: OptionalStr = None
    description: OptionalStr = None


class ResearchPriorityPayload(BaseModel):
    az: Optional[ResearchPriorityTranslation] = None
    en: Optional[ResearchPriorityTranslation] = None


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
    links: Optional[List[ResearchLinkPayload]] = None

    class Config:
        extra = "ignore"


class PublishResearchPage(BaseModel):
    is_active: bool
