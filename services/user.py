
from datetime import datetime
from datetime import datetime
from models.user import User  
from auth.password import hash_password
from schemas.users import SignupSchema


def create_user(data: SignupSchema):
    # check if user already exists
    existing = User.match_nodes(filters={"email__iexact": data.email})
    if existing:
        raise ValueError("User already exists")

    user = User(
        id=data.email,                      # or uuid4()
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_active=True,
    )

    user.merge()
    return user