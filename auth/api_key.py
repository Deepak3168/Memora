import secrets
import hashlib
from datetime import datetime, timedelta


def generate_api_key_helper(user_id: str, days_valid: int = 30, name: str = ""):
    """
    Generate API key components for a user without creating a node yet.

    Returns:
        random_part (str): random string stored in node
        api_key (str): hashed API key for client
        expires_at (datetime): expiration datetime
    """
    random_part = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=days_valid)

    # Deterministic hash for the API key
    base_string = f"{user_id}:{int(expires_at.timestamp())}:{random_part}"
    api_key = hashlib.sha256(base_string.encode()).hexdigest()

    return random_part, api_key, expires_at


