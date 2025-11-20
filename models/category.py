from typing import ClassVar, List, Optional
from datetime import datetime
from neontology import  BaseNode
 



class CategoryNode(BaseNode):
    __primarylabel__: ClassVar[str] = "Category"
    __primaryproperty__: ClassVar[str] = "id"


    id: str
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: datetime = datetime.utcnow()
    last_updated: datetime = datetime.utcnow()
    remarks: Optional[str] = None   