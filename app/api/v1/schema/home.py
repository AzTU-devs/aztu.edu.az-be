"""Request bodies for the Home section.

The page is a singleton (``page_key = "home"``) with two ordered metric lists —
a "hero" strip and a "numbers" grid — saved together in one PUT, exactly like
the About module. Each list is sent whole and replaces what is stored, which is
what the dashboard's single Save button does.

Optional text uses ``OptionalStr`` because the admin forms submit "" for
anything left blank, and a bare ``str | None`` would 422 on that.
"""

from typing import List, Optional

from pydantic import BaseModel

from app.api.v1.schema.common import OptionalStr


class HomeMetricTranslation(BaseModel):
    label: OptionalStr = None
    sublabel: OptionalStr = None


class HomeMetricPayload(BaseModel):
    value: OptionalStr = None
    suffix: OptionalStr = None
    az: Optional[HomeMetricTranslation] = None
    en: Optional[HomeMetricTranslation] = None


class UpdateHomePage(BaseModel):
    # Omit a key to leave that list untouched; send [] to clear it.
    hero_metrics: Optional[List[HomeMetricPayload]] = None
    number_metrics: Optional[List[HomeMetricPayload]] = None

    class Config:
        extra = "ignore"


class PublishHomePage(BaseModel):
    is_active: bool
