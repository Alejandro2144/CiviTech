
from typing import List
from pydantic import BaseModel, HttpUrl


class TransferPayload(BaseModel):
    id: int
    citizenName: str
    citizenEmail: str
    urlDocuments: dict
    confirmAPI: HttpUrl


class UserDataPayload(BaseModel):
    id: int
    citizenName: str
    citizenEmail: str

class InitialTransferPayload(BaseModel):
    transferAPIURL: HttpUrl

class confirmTransferPayload(BaseModel):
    id: int
    req_status: int
    confirmAPIURL: HttpUrl

class ConfirmPayload(BaseModel):
    id: int
    req_status: int