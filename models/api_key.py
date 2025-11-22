from typing import ClassVar
from datetime import datetime, timedelta
import secrets
import hashlib
from .user import User
from neontology import BaseNode


class APIKey(BaseNode):
    __primarylabel__: ClassVar[str] = "APIKey"
    __primaryproperty__: ClassVar[str] = "api_key"

    id: str  
    name: str 
    api_key : str 
    random_part: str 
    created_at: datetime = datetime.utcnow()
    expires_at: datetime = datetime.utcnow() + timedelta(days=30)

    # -----------------------------
    # Generate new API key
    # -----------------------------
    # @classmethod
    # def generate(cls, user: User, name: str = "", days_valid: int = 30) -> ("APIKey", str):
    #     """
    #     Generate a new APIKey node and return the instance + raw API key
    #     """
    #     random_part = secrets.token_urlsafe(32)
    #     expires_at = datetime.utcnow() + timedelta(days=days_valid)

    #     # Construct deterministic API key
    #     base_string = f"{user.id}:{int(expires_at.timestamp())}:{random_part}"
    #     api_key = hashlib.sha256(base_string.encode()).hexdigest()

    #     instance = cls(
    #         id=str(secrets.randbits(64)),
    #         user=user,
    #         name=name,
    #         random_part=random_part,
    #         created_at=datetime.utcnow(),
    #         expires_at=expires_at
    #     )
    #     instance.merge()

    #     return instance, api_key

    # -----------------------------
    # Verify API key
    # -----------------------------
    # def verify(self, provided_key: str) -> bool:
    #     """
    #     Verify a given API key against this node
    #     """
    #     if datetime.utcnow() > self.expires_at:
    #         return False

    #     base_string = f"{self.user.id}:{int(self.expires_at.timestamp())}:{self.random_part}"
    #     expected_key = hashlib.sha256(base_string.encode()).hexdigest()
    #     return expected_key == provided_key

    # # -----------------------------
    # # Refresh key (optional)
    # # -----------------------------
    # def refresh(self, days_valid: int = 30) -> str:
    #     """
    #     Refresh the API key: generates new random_part and new expiry
    #     Returns new raw API key
    #     """
    #     self.random_part = secrets.token_urlsafe(32)
    #     self.expires_at = datetime.utcnow() + timedelta(days=days_valid)

    #     base_string = f"{self.user.id}:{int(self.expires_at.timestamp())}:{self.random_part}"
    #     new_api_key = hashlib.sha256(base_string.encode()).hexdigest()
    #     return new_api_key
