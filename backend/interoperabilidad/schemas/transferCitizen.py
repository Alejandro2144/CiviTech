from pydantic import BaseModel

class TransferPayload(BaseModel):
    id: int
    citizenName: str
    citizenEmail: str
    urlDocuments: dict
    confirmAPI: str

class UserDataPayload(BaseModel):
    id: int
    citizenName: str
    citizenEmail: str

class InitialTransferPayload(BaseModel):
    transferAPIURL: str

class confirmTransferPayload(BaseModel):
    id: int
    req_status: int
    confirmAPI: str

class ConfirmPayload(BaseModel):
    id: int
    req_status: int