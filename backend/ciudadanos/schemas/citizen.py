from pydantic import BaseModel, EmailStr
from typing import Optional

class CitizenBase(BaseModel):
    id: int
    name: str
    address: str
    email: EmailStr

class CitizenCreate(CitizenBase):
    password: str

class CitizenResponse(CitizenBase):
    civi_email: EmailStr
    access_token: Optional[str] = None

    class Config:
        orm_mode = True

class CitizenLogin(BaseModel):
    email: EmailStr
    password: str
