import uuid

def generate_id() -> str:
    """Generate a unique ID for documents or chunks."""
    return str(uuid.uuid4())
