from pydantic import BaseModel

class SetPasswordRequest(BaseModel):
    token: str
    password: str

class SetPasswordResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
