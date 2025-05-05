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
    access_token: str

    class Config:
        from_attributes = True

class CitizenProfileResponse(CitizenBase):
    civi_email: EmailStr

    class Config:
        from_attributes = True

class CitizenLogin(BaseModel):
    email: EmailStr
    password: str
