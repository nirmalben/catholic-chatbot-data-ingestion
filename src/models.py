from typing import Dict, Any
from pydantic import BaseModel

class Document(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}