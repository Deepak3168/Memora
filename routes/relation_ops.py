from fastapi import APIRouter, HTTPException
from schemas.create_relation import RelationCreate
from models.entity import EntityNode
from models.relation import RelationEdge

router = APIRouter(prefix="/relation", tags=["Relation"])

@router.post("/",operation_id="create_realtionship",summary="this tool is used to create relationship by connecting source entity to target entity and giving type of relation ship , and strength between two nodes and possible remarks")
async def create_relation(data: RelationCreate):

    src = EntityNode.match(data.source_id)
    tgt = EntityNode.match(data.target_id)

    if not src or not tgt:
        raise HTTPException(status_code=404, detail="One or both entities not found")

    try:
        rel = RelationEdge(
            source=src,
            target=tgt,
            type=data.type,
            strength=data.strength,
            remarks=data.remarks
        )
        rel.merge()
        return {"status": "ok", "relation": rel.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
