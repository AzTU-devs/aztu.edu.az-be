from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile, Form, Depends

class CreateMenu(BaseModel):
    category_id: int
    az_title: str
    en_title: str
    url: Optional[str]

class CreateMenuItem(BaseModel):
    az_title: str
    en_title: str
    url: str

class AddMenuItems(BaseModel):
    menu_id: int
    items: List[CreateMenuItem]