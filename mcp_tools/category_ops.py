
from models.category import CategoryNode
from fastapi import APIRouter,HTTPException,Depends
from auth.dependencies import user_by_token
from schemas.relation import CategoryCreate
from models.user import User 
from models.relations import HAS_CATEGORY
from neontology import GraphConnection

category_router = APIRouter(prefix="/category",tags=["Category"])



@category_router.post(
    path="/",
    summary="Create a new Category and associate it with the user",
    description=(
        "Create a new Category with a unique ID, name, and optional fields such as "
        "description, tags, and remarks. "
        "The new Category will be automatically linked to the authenticated user. "
        "The request body should follow the `CategoryCreate` model, which ensures all "
        "fields are validated and processed efficiently. "
        "This endpoint is designed to prevent clients from manually specifying the ID, "
        "ensuring it is always generated server-side."
    ),
)
def create_category(data: CategoryCreate,user:User =Depends(user_by_token)):
    category_created = CategoryNode(**data.model_dump())
    category = category_created.create()
    related = HAS_CATEGORY(source=user,target=category)
    related.merge()

    return {"message":"Category Created"}

@category_router.get(
    path="/list",
    summary="Retrieve all Categories associated with the authenticated user",
    description=(
        "Fetch a list of all Categories that belong to the authenticated user. "
        "Each Category in the response includes its ID and name. "
        "This allows the client to view all available Categories for selection, "
        "navigation, or further processing within the system."
    )
)
def get_categories(user:User = Depends(user_by_token)):
    gc = GraphConnection()

    user_id = user.id 

    cypher_query = f"""
        MATCH (u:User {{id: '{user_id}'}})-[:HAS_CATEGORY]->(c:Category)
        RETURN COLLECT({{name: c.name, id: c.id}}) AS category_list;
        """
    result = gc.evaluate_query_single(cypher_query)
    return result



# 7347328438