from pydantic import BaseModel
from typing import Optional

class RelationCreate(BaseModel):
    source_id: str
    target_id: str
    type: str
    strength: float = 0.5
    remarks: Optional[str] = None
