import json
from typing import Any

def serialize_job(data: Any) -> str:
    """Serialize job data to JSON."""
    return json.dumps(data)

def deserialize_job(data: str) -> Any:
    """Deserialize job data from JSON."""
    return json.loads(data)