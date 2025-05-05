from pydantic import BaseModel, EmailStr

class CitizenBase(BaseModel):
    id: int
    name: str
    address: str
    email: EmailStr

class CitizenCreate(CitizenBase):
    password: str 

class CitizenResponse(CitizenBase):
    civi_email: EmailStr

    class Config:
        orm_mode = True

class CitizenLogin(BaseModel):
    email: EmailStr
    password: str

