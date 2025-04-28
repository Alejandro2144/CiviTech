from pydantic import BaseModel, EmailStr

class CitizenRegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    id_type: str
    id_number: str
    birth_date: str  # formato esperado YYYY-MM-DD
    address: str

class CitizenRegistrationResponse(BaseModel):
    message: str
    assigned_email: EmailStr
