
from typing import List
from pydantic import BaseModel, HttpUrl


class TransferPayload(BaseModel):
    id: int
    citizenName: str
    citizenEmail: str
    urlDocuments: dict