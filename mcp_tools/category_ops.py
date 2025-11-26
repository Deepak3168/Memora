
from models.category import CategoryNode
from fastapi import APIRouter,HTTPException,Depends
from auth.dependencies import user_by_token
from schemas.relation import CategoryCreate
from models.user import User 
from models.relations import HAS_CATEGORY
category_router = APIRouter(prefix="/category",tags=["Category"])



@category_router.post(
    path="/",
    summary="Create a new category and link it to the user",
    description=(
        "Creates a category and connects it to the authenticated user. "
        "The request body uses the CategoryCreate model, which allows all fields "
        "to be read and validated at once for efficient processing."
    ),
)
def create_category(data: CategoryCreate,user:User =Depends(user_by_token)):
    category_created = CategoryNode(**data.model_dump())
    category = category_created.create()
    related = HAS_CATEGORY(source=user,target=category)
    related.merge()

    return {"message":"Category Created"}