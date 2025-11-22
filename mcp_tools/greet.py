from fastapi import APIRouter
from fastapi import Depends
from models.user import User 
from auth.dependencies import user_by_token



greet_router = APIRouter(prefix="/greet", tags=["Greet"])

@greet_router.get("/{name}",operation_id="greet")
def greet(name: str,
          user: User = Depends(user_by_token)) -> dict:
    username = user.username
    return {"message":f"Hello, {name}! Welcome to Memora MCP Server.",
            "username":username}