from typing import ClassVar, Optional
from datetime import datetime
from .entity import EntityNode
from neontology import  BaseRelationship

class RelationEdge(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "RELATION"

    source: EntityNode
    target: EntityNode
    type: str
    strength: float = 0.5
    remarks: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    last_updated: datetime = datetime.utcnow()
