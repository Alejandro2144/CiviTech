
from typing import List
from pydantic import BaseModel, HttpUrl


class URLDocuments(BaseModel):
    URL1: List[HttpUrl]
    URL2: List[HttpUrl]

class TransferPayload(BaseModel):
    id: int
    citizenName: str
    citizenEmail: str
    urlDocuments: URLDocuments