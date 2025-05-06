from pydantic import BaseModel
from typing import Optional

class DocumentMetadata(BaseModel):
    user_id: str
    document_type: str
    description: Optional[str] = None
