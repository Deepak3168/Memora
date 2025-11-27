from models.entity import EntityNode
from models.user import User
from models.category import CategoryNode
from schemas.entity_ops import EntityCreate
from fastapi import APIRouter,Depends,Query,HTTPException
from auth.dependencies import user_by_token
from models.relation import RelationEdge
from models.relations import *
from neontology import GraphConnection

entity_router = APIRouter(
    prefix = '/entity',
    tags = ["Entity"]
)


@entity_router.post(
    path="/",
    summary="Create an Entity with optional relationships, including custom ones",
    description=(
        "Create a new Entity with a unique ID and name. "
        "Optionally, you can relate this Entity to an existing Category or another Entity. "
        "If the exact Category does not exist, you can create a custom relationship by providing "
        "`type` (the relationship type), `strength` (numeric value indicating importance), "
        "and `remarks` (optional notes about the relationship). "
        "All relationships will be automatically created in the graph."
    )
)
def create_entity(
    data: EntityCreate,
    user: User = Depends(user_by_token),

    # Entity → Category
    category_name: str | None = Query(
        None, description="Name of the Category to relate with"
    ),

    # Entity → Entity
    target_entity_id: str | None = Query(
        None, description="Name of another Entity to relate with"
    ),

    # Inbuilt relationship class
    relation_name: str | None = Query(
        None,
        description="Name of the relation class. "
                    "If using a custom relation, omit this."
    ),

    # 🔶 Custom Relation (separate scalar params)
    custom_type: str | None = Query(
        None, description="Custom relation type"
    ),
    custom_strength: float | None = Query(
        None, description="Custom relation strength (float)"
    ),
    custom_description: str | None = Query(
        None, description="Custom relation description"
    ),
    custom_remarks: str | None = Query(
        None, description="Custom relation remarks"
    ),
):
    """
    Steps:
    1. Create Entity
    2. If category_name is provided → relate entity → category
    3. If target_entity_name is provided → relate entity → target entity
    4. If relation_name is provided → use relationship class
    5. Else if custom_type is provided → create custom free-form relation
    """
    user_id = user.id
    # ---------------------------------------------------------
    # 1. Create the Entity
    # ---------------------------------------------------------
    entity_created = EntityNode(**data.model_dump())
    entity = entity_created.create()

    # Build custom relation dict only if user provided fields
    custom_relation = None
    custom_relation = {"type": custom_type}  # mandatory

    if custom_strength is not None:
        custom_relation["strength"] = custom_strength

    if custom_description is not None:
        custom_relation["description"] = custom_description

    if custom_remarks is not None:
        custom_relation["remarks"] = custom_remarks

    # ---------------------------------------------------------
    # 2. Entity → Category Relation
    # ---------------------------------------------------------
    if category_name:
        gc = GraphConnection()

        cypher_query = f"""
            MATCH (u:User {{id: '{user_id}'}})-[:HAS_CATEGORY]->(c:Category {{name: '{category_name}'}})
            RETURN c.id;
        """

        category_id = gc.evaluate_query_single(cypher_query)
        category = CategoryNode.match(category_id)

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Inbuilt relationship class
        if relation_name:
            RelationClass = BaseRelation.get_subclass(relation_name)
            RelationClass(source=entity, target=category).merge()

        # Custom Relationship
        elif custom_relation:
            RelationEdge(
                **custom_relation,
                source=entity,
                target=category
            ).merge()

    # ---------------------------------------------------------
    # 3. Entity → Entity Relation
    # ---------------------------------------------------------
    if target_entity_id:
        target_entity = EntityNode.match(target_entity_id)
        if not target_entity:
            raise HTTPException(status_code=404, detail="Target entity not found")

        # Inbuilt relationship class
        if relation_name:
            RelationClass = BaseRelation.get_subclass(relation_name)
            RelationClass(source=entity, target=target_entity).merge()

        # Custom Relationship
        elif custom_relation:
            RelationEdge(
                **custom_relation,
                source=entity,
                target=target_entity
            ).merge()

    # ---------------------------------------------------------
    # Return
    # ---------------------------------------------------------
    return {
        "message": "Entity created successfully",
        "entity": entity
    }



@entity_router.get(
    path="/list",
    summary="Fetch a subgraph of entities and relationships for a given Category",
    description=(
        "Retrieve a subgraph containing all entities and their relationships that are "
        "connected to a specific Category, identified by its ID. "
        "The response includes: "
        "1. Category details (ID and name), "
        "2. All related entities (ID and name), "
        "3. All relationships between these entities (source ID and target ID). "
        "This allows you to explore the structure and connections of a Category in the graph."
    )
)
def get_sub_graph_by_category_id(category_id:str | None = Query(None,description="Category ID"),user:User = Depends(user_by_token)):
    if category_id is None:
        return HTTPException(status_code=400,detail="Category ID is Required")
    gc = GraphConnection()

    cypher_query = f"""
        MATCH (c:Category {{ id: '{category_id}' }})
        MATCH p = (c)-[*]-(e:Entity)
        WITH c,
            collect(DISTINCT e) AS entities,
            collect(DISTINCT p) AS paths

        UNWIND paths AS path
        UNWIND relationships(path) AS rel

        WITH c,
            entities,
            collect(DISTINCT {{
                source: startNode(rel).id,
                target: endNode(rel).id
            }}) AS relationships

        RETURN 
            {{ id: c.id, name: c.name }} AS category,
            [ent IN entities | {{ id: ent.id, name: ent.name }}] AS entities,
            relationships;
        """
    
    results = gc.evaluate_query(cypher_query)

    if hasattr(results, "records_raw"):
        records = results.records_raw
    elif hasattr(results, "records"):
        records = results.records
    else:
        raise ValueError("Could not find records field in NeontologyResult")
    
    return records


@entity_router.get(
    path="/list/all",
    summary="Fetch all entities with pagination",
    description=(
        "Retrieve a list of all entities in the system. "
        "Each entity includes its ID and name. "
        "The results are paginated, with a default page size of 25. "
        "You can specify the page number using the `page` query parameter. "
        "The response also includes `next` and `prev` links to navigate through pages easily."
    )
)
def get_all_entities(
    page: int = Query(1, description="Page number, default is 1"),
    user: User = Depends(user_by_token)
):
    PAGE_SIZE = 25
    skip = (page - 1) * PAGE_SIZE
    limit = PAGE_SIZE

    cypher_query = """
    MATCH (n:Entity)
    RETURN {id: n.id, name: n.name} AS entity
    ORDER BY n.id
    SKIP $skip
    LIMIT $limit
    """

    gc = GraphConnection()
    
    results = gc.evaluate_query(cypher_query, params={"skip": skip, "limit": limit})
    entities = results.records_raw if hasattr(results, "records_raw") else []

    # Determine next and prev page numbers
    next_page = page + 1 if len(entities) == PAGE_SIZE else None
    prev_page = page - 1 if page > 1 else None

    # Construct links
    base_url = "/list/all"
    links = {}
    if next_page:
        links["next"] = f"{base_url}?page={next_page}"
    if prev_page:
        links["prev"] = f"{base_url}?page={prev_page}"

    return {
        "page": page,
        "page_size": PAGE_SIZE,
        "entities": entities,
        "links": links
    }

    