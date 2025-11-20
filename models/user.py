from typing import ClassVar, List, Optional
from datetime import datetime
from neontology import  BaseNode 



class User(BaseNode):
    __primarylabel__: ClassVar[str] = "User"
    __primaryproperty__: ClassVar[str] = "id"

    id: str
    username: str
    email: str
    hashed_password: str
    roles: Optional[List[str]] = None
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    last_login: Optional[datetime] = None
    last_logout_at: Optional[datetime] = None   # <—
    last_updated: datetime = datetime.utcnow()
    remarks: Optional[str] = None


