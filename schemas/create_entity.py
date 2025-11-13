from pydantic import BaseModel
from typing import Optional, List

class EntityCreate(BaseModel):
    id: str
    name: str
    labels: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    remarks: Optional[str] = None
