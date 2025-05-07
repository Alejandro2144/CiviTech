from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class DocumentMetadata(BaseModel):
    idDocument: str = Field(default_factory=lambda: str(uuid.uuid4()))
    idCitizen: str
    documentTitle: str
    urlDocument: Optional[str] = None
    uploadDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    documentType: Optional[str] = "document"
    isCertified: Optional[bool] = False
    authenticationStatus: Optional[str] = "pending"
    authenticationDate: Optional[datetime] = None
    accessControlList: Optional[List[str]] = []
