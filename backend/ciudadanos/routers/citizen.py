from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.citizen import CitizenCreate, CitizenResponse, CitizenLogin
from ..services.citizen_service import CitizenService
from ..config.db import get_db

router = APIRouter(prefix="/citizens", tags=["Citizens"])

@router.post("/", response_model=CitizenResponse)
async def register_citizen(citizen: CitizenCreate, db: Session = Depends(get_db)):

    service = CitizenService(db)

    try:
        citizen_db = await service.register_citizen(citizen)
        return CitizenResponse(
            id=citizen_db.id,
            name=citizen_db.name,
            address=citizen_db.address,
            email=citizen_db.email,
            civi_email=citizen_db.civi_email
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=CitizenResponse)
def login(citizen_login: CitizenLogin, db: Session = Depends(get_db)):

    service = CitizenService(db)
    citizen = service.authenticate_citizen(citizen_login.email, citizen_login.password)

    if not citizen:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return CitizenResponse(
        id=citizen.id,
        name=citizen.name,
        address=citizen.address,
        email=citizen.email,
        civi_email=citizen.civi_email
    )
