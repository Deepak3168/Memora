from typing import ClassVar, List, Optional
from datetime import datetime
from neontology import  BaseNode

class EntityNode(BaseNode):
    __primarylabel__: ClassVar[str] = "Entity"
    __primaryproperty__: ClassVar[str] = "id"

    id: str
    name: str
    labels: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    remarks: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    last_updated: datetime = datetime.utcnow()


