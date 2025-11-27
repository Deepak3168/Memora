from pydantic import BaseModel, Field
from typing import Optional, List
from utils.primary_key import generate_prefixed_uuid

class EntityCreate(BaseModel):
    id: str = Field(default_factory=lambda: generate_prefixed_uuid("ENT"), exclude=True)
    name: str
    labels: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    remarks: Optional[str] = None
