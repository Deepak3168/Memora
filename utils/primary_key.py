import uuid

def generate_prefixed_uuid(prefix: str) -> str:
    """
    Returns IDs like ENT-550e8400-e29b-41d4-a716-446655440000
    """
    if not (prefix and len(prefix) == 3 and prefix.isalpha()):
        raise ValueError("Prefix must be exactly 3 alphabetic letters.")
    
    return f"{prefix.upper()}-{uuid.uuid4()}"
