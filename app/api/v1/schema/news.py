from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import Query, UploadFile, Form, Depends



class ReOrderNews(BaseModel):
    news_id: int
    new_order: int

class NewsGetter(BaseModel):
    category_id: int | None = None
    start: int | None = Field(default=0, ge=0, description="Start index")
    end: int | None = Field(default=10, gt=0, description="End index")
