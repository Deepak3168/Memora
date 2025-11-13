from fastapi import APIRouter, HTTPException
from schemas.create_entity import EntityCreate
from models.entity import EntityNode
from typing import List

router = APIRouter(prefix="/entity", tags=["Entity"])

@router.post("/",operation_id="create_entity",summary="this tool is used to create a entity node by passing name:str,labels:list[str],keywords:list[str],remarks:str")
async def create_entity(data: EntityCreate):
    try:
        node = EntityNode(**data.model_dump())
        node.create()
        return {"status": "ok", "entity": node.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/entities", response_model=List[EntityNode],operation_id="get_all_entities",summary="this tool is used to get all entity nodes present in the database")
def get_all_entities():
    nodes = EntityNode.match_nodes() 
    return nodes
