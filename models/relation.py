from typing import ClassVar, Optional,Union
from datetime import datetime
from .entity import EntityNode
from .category import CategoryNode
from neontology import  BaseRelationship

class RelationEdge(BaseRelationship):
    __relationshiptype__: ClassVar[str] = "RELATION"

    source: Union[EntityNode, CategoryNode]
    target: Union[EntityNode, CategoryNode]
    type: str
    strength: float = 0.5
    remarks: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    last_updated: datetime = datetime.utcnow()
