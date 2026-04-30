from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class KnowledgeSourceCreate(BaseModel):
    url: str
    label: Optional[str] = None


class KnowledgeSourceResponse(BaseModel):
    id: int
    url: str
    label: Optional[str]
    is_active: bool
    last_scraped_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}
