from fastapi import APIRouter, HTTPException
from schemas.users import LoginSchema
from auth.password import verify_password
from models.user import User
from auth.jwt import issue_token
from fastapi import Header
from auth.jwt import verify_token
from datetime import datetime
from fastapi import Depends
from auth.dependencies import get_current_user
from services.user import create_user
from schemas.users import SignupSchema




auth_router = APIRouter(prefix="/auth", tags=["Authentication"])




@auth_router.post("/login")
def login(data: LoginSchema):

    user = User.match_nodes(filters={"email__iexact": data.email})
    user = user[0]
    if not user:
        raise HTTPException(401, "Invalid credentials")

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



@auth_router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"user": user}



@auth_router.post("/signup")
def signup(data: SignupSchema):
    try:
        user = create_user(data)
        return {"message": "User created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
   