
import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from models.user import User
from constants import constants


SECRET = constants.JWT_SECRET
ALGO = constants.JWT_ALGORITHM
EXPIRE_MINUTES = constants.JWT_EXPIRE_MINUTES




def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    iat = datetime.utcnow()
    to_encode.update({"exp": expire,"iat":iat})
    

    return jwt.encode(to_encode, SECRET, algorithm=ALGO)


def issue_token(sub: str) -> str:
    token = create_access_token({"sub": sub})
    return token


# auth/jwt.py

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
    except Exception:
        return None

    user_id = payload["sub"]
    token_iat = payload["iat"]

    # Correct Neontology query
    user = User.match(user_id)
    if not user:
        return None

    # Check logout state
    if user.last_logout_at:
        if token_iat < int(user.last_logout_at.timestamp()):
            return None

    return payload