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


def user_by_token(secret: str = Header(None, alias="API_KEY")):
    if not secret:
        raise HTTPException(status_code=401, detail="Missing API_KEY header")

    key = secret  

    api_key_obj = APIKey.match(key)
    if not api_key_obj:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # expiration validation
    if datetime.utcnow() > api_key_obj.expires_at:
        raise HTTPException(status_code=401, detail="API key expired")

    # ---- Fetch user through GENERATED_FOR relation ----
    gc = GraphConnection()

    cypher_query = f"""
        MATCH (api:APIKey {{api_key: '{key}'}})-[:GENERATED_FOR]->(u:User)
        RETURN COLLECT({{user_id: u.id}}) AS users
    """

    result = gc.evaluate_query_single(cypher_query)

    if not result or not result[0]["user_id"]:
        raise HTTPException(status_code=401, detail="User not found for token")

    user_id = result[0]["user_id"]

    # Neo4j-OGM lookup
    user = User.match(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
