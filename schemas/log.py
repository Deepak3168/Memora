from pydantic import BaseModel
from typing import Optional, List


class LogCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: Optional[str] = None
    links: Optional[str] = None
    tags: Optional[str] = None


class LogResponse(BaseModel):
    log_id: int
    user_id: int
    date: str
    title: str
    description: Optional[str]
    type: Optional[str]
    links: Optional[str]
    tags: Optional[str]
