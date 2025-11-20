# auth/dependencies.py
from fastapi import Depends, HTTPException, Header
from auth.jwt import verify_token

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload  # contains email, username etc.


# curl -X GET \
#   http://127.0.0.1:8001/auth/profile \
#   -H "accept: application/json" \
#   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWVwYWtAZXhhbXBsZS5jb20iLCJleHAiOjE3NjM1NDc3MDB9.2CWa4zPS5n6eaiT4w-P0cIcIWGnkArAc_7njlJ5RNcU"
