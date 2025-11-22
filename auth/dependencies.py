# auth/dependencies.py
from fastapi import Depends, HTTPException, Header
from auth.jwt import verify_token
from models.user import User
from models.api_key import APIKey
from datetime import datetime, timedelta
from models.relations import GENERATED_FOR
import hashlib
import logging 
from neontology import GraphConnection

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)  

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = User.match(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user_id


# curl -X GET \
#   http://127.0.0.1:8001/auth/profile \
#   -H "accept: application/json" \
#   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWVwYWtAZXhhbXBsZS5jb20iLCJleHAiOjE3NjM1NDgwNDksImlhdCI6MTc2MzU0NjI0OX0.C_lXmD3FNaVq4B8TmBHtrHeXPAgoT7lykoqUfYYHQjw"


# curl -X POST \
#   http://127.0.0.1:8001/auth/logout \
#   -H "accept: application/json" \
#   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWVwYWtAZXhhbXBsZS5jb20iLCJleHAiOjE3NjM1NDgwNDksImlhdCI6MTc2MzU0NjI0OX0.C_lXmD3FNaVq4B8TmBHtrHeXPAgoT7lykoqUfYYHQjw"


def user_by_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    key = authorization.replace("Bearer ", "")


    if key is None :
        HTTPException(status_code=401, detail="API key not found")

    api_key = APIKey.match(key)

    logging.info(f"api_key:{api_key}")

    if not api_key :
        HTTPException(status_code=401, detail="Invalid token")

    if datetime.utcnow() > api_key.expires_at :
        return HTTPException(status_code=401, detail="Invalid token")
    

    gc = GraphConnection()

    cypher_query = f"""
    MATCH (api:APIKey {{api_key: '{api_key}'}})-[:GENERATED_FOR]->(u:User)
    RETURN COLLECT({{user_id: u.id}}) AS users
    """

    result = gc.evaluate_query_single(cypher_query)


    users = result
    user_id = users[0]["user_id"] if users else None

    logging.info("result",result)
    
    user = User.match(user_id)

    logging.info("user",user.username)

    return user
