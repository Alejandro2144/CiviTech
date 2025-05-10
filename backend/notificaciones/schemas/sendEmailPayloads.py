from pydantic import BaseModel

class PasswordEmailPayload(BaseModel):
    action: str
    citizenName: str
    citizenEmail: str
    passwordSetURL: str


class InFileActionEmailPayload(BaseModel):
    action: str
    citizenEmail: str
    action: str
    fileName: str
