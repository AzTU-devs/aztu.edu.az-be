from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile, Form, Depends

class ReOrderCollaboration(BaseModel):
    collaboration_id: int
    new_order: int