from models.category import CategoryNode
from pydantic import BaseModel
from typing import Optional, List



class CategoryCreate(BaseModel):
    name:str
    description:Optional[str]=None
    tags:Optional[List[str]]=None
    remarks:Optional[str]=None


# {
#   "name": "Finance",
#   "description": "A category for managing financial matters, budgets, and money-related information",
#   "remarks": "Primary finance tracking category",
#   "tags": ["money", "budget", "expenses", "income"]
# }