from fastapi import APIRouter, HTTPException,Query
from schemas.users import LoginSchema
from auth.password import verify_password
from models.user import User
from models.api_key import APIKey
from utils.categories import create_and_connect_categories
from auth.jwt import issue_token
from fastapi import Header
from auth.jwt import verify_token
from datetime import datetime
from fastapi import Depends
from auth.dependencies import get_current_user
from services.user import create_user
from schemas.users import SignupSchema
from datetime import timedelta, datetime
from auth.api_key import generate_api_key_helper
import secrets 
from models.relations import GENERATED_FOR
from task import executor

from concurrent.futures import ThreadPoolExecutor
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])




@auth_router.post("/login")
def login(data: LoginSchema):

    user = User.match_nodes(filters={"email__iexact": data.email})
    if not user:
        raise HTTPException(401, "Invalid credentials")

    user = user[0]

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = issue_token(sub=user.id)
    return {"access_token": token}




@auth_router.post("/logout")
def logout(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing Authorization header")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")

    user = User.match(payload["sub"])
    user.last_logout_at = datetime.utcnow()
    user.save()

    return {"message": "Logged out"}



# @auth_router.get("/profile")
# def profile(user,payload=Depends(get_current_user)):

#     return {"user": payload}



@auth_router.post("/signup")
def signup(data: SignupSchema):
    try:
        user = create_user(data)
        categories = create_and_connect_categories(user)
        return {"message": "User created","categories":categories}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    



@auth_router.post("/api_key")
def generate_api_key(
    name: str = Query(..., description="Descriptive name for the API key"),
    days_valid: int = Query(30, ge=1, le=365, description="Number of days the key is valid"),
    user_id: str = Depends(get_current_user)
):
    """
    Generate a new API key for the current user using a helper function.
    """
    # Generate random part, hashed key, and expiration
    random_part, hashed_key, expires_at = generate_api_key_helper(
        user_id=user_id,
        days_valid=days_valid,
        name=name
    )
    user = User.match(user_id)
    
    # Create APIKey node
    api_key_node = APIKey(
        id=str(secrets.randbits(64)),
        name=name,
        random_part=random_part,
        api_key=hashed_key,
        created_at=datetime.utcnow(),
        expires_at=expires_at
    )

    # Persist node
    api = api_key_node.create()


    relation = GENERATED_FOR(
        source=api,
        target = user
    )


    relation.merge()
    
    executor.submit(create_and_connect_categories, user)


    # Return the hash to the client
    return {
        "api_key": hashed_key,  # this is what client will use
        "name": name,
        "expires_at": expires_at.isoformat()
    }
