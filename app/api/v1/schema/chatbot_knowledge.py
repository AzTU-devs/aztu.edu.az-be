from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional
from datetime import datetime


class KnowledgeSourceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    label: Optional[str] = None


class KnowledgeSourceResponse(BaseModel):
    id: int
    url: str
    label: Optional[str]
    is_active: bool
    last_scraped_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
