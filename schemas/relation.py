from models.category import CategoryNode
from pydantic import BaseModel,Field
from typing import Optional, List
from utils.primary_key import generate_prefixed_uuid


class CategoryCreate(BaseModel):
    # id:str =  Field(default_factory=lambda: generate_prefixed_uuid("CAT"),exclude=True)
    name:str
    description:Optional[str]=None
    tags:Optional[List[str]]=None
    remarks:Optional[str]=None


class RelationCreate(BaseModel):
    type : str
    strength : float = 0.5
    remarks : Optional[str]= None

# {
#   "name": "Finance",
#   "description": "A category for managing financial matters, budgets, and money-related information",
#   "remarks": "Primary finance tracking category",
#   "tags": ["money", "budget", "expenses", "income"]
# }