from models.relation import RelationEdge
from fastapi import APIRouter,Depends,Query,HTTPException,Body
from auth.dependencies import user_by_token
from models.user import User
from schemas.relation import RelationCreate
from models.category import CategoryNode
from models.entity import EntityNode
from models.relations import BaseRelation

relation_router  = APIRouter(prefix="/relation",tags=["Relation"])


@relation_router.get(
    path="/list",
    summary="Retrieve all available relation types",
    description=(
        "Fetch a list of all relation types currently defined in the system. "
        "Each item in the response includes the class name of the relation. "
        "This endpoint helps clients understand what types of relationships can be created "
        "between entities or categories."
    )
)
def get_relations(user:User=Depends(user_by_token)):
    return [
        "BELONGS TO",
        "OWNS",
        "USES",
        "REQUIRES",
        "RELATED_TO",
        "PART_OF",
        "DERIVED_FROM",
        "MENTIONS",
        "WORKS_ON",
        "LEARNED",
        "INTRESTED_IN"
    ]


@relation_router.post(
    path="/",
    summary="Create a relation edge between entities or categories",
    description=(
        "Create a new relationship (edge) between two nodes in the graph, which can be "
        "either a built-in relation type or a custom relation. "
        "For custom relations, you can provide `type` (relation name), `strength` (numeric importance), "
        "and `remarks` (optional notes). "
        "This endpoint ensures that the relationship is properly created and stored in the graph."
    )
)
def create_relation(
    data: RelationCreate | None = Body(None),
    relation_name: str | None = Query(None),
    custom: bool | None = Query(None),
    source_id: str | None = Query(None),
    target_id: str | None = Query(None),
    user: User = Depends(user_by_token)
):

    # --- Source Node ---
    if source_id is None:
        raise HTTPException(400, "source_id is required")

    if source_id.startswith("CAT"):
        source = CategoryNode.match(source_id)
    elif source_id.startswith("ENT"):
        source = EntityNode.match(source_id)
    else:
        raise HTTPException(400, "Invalid source_id format")

    if not source:
        raise HTTPException(404, "Source node not found")


    # --- Target Node ---
    if target_id is None:
        raise HTTPException(400, "target_id is required")

    if target_id.startswith("CAT"):
        target = CategoryNode.match(target_id)
    elif target_id.startswith("ENT"):
        target = EntityNode.match(target_id)
    else:
        raise HTTPException(400, "Invalid target_id format")

    if not target:
        raise HTTPException(404, "Target node not found")


    # --- Custom Relation ---
    if custom:
        if data is None:
            raise HTTPException(
                400,
                "Custom relation requires: type (mandatory), optional strength/description/remarks"
            )

        relation = RelationEdge(
            **data.model_dump(exclude_none=True),
            source=source,
            target=target
        )
        relation.merge()
        return {"message": "Custom relation created"}


    # --- Built-in Relation ---
    else:
        if relation_name is None:
            raise HTTPException(400, "relation_name is required for built-in relation")

        try:
            RelationClass = BaseRelation.get_subclass(relation_name)
        except KeyError:
            raise HTTPException(400, f"Unknown relation type: {relation_name}")

        RelationClass(source=source, target=target).merge()
        return {"message": "Built-in relation created"}






