from pydantic import BaseModel

class TokenRequest(BaseModel):
    id: int
    name: str
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    id: int
    name: str
    email: str
    exp: int
