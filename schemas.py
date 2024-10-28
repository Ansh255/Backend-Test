# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    original_url: str
    expires_at: Optional[datetime] = None

class URLResponse(BaseModel):
    short_url: str
    original_url: str
    created_at: datetime
    expires_at: Optional[datetime] = None
