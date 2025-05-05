from pydantic import BaseModel

class TokenRequest(BaseModel):
    id: int
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    id: int
    email: str
    exp: int
