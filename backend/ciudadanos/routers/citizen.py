from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.citizen import CitizenCreate, CitizenResponse, CitizenLogin, CitizenProfileResponse, UserIdPayload
from services.citizen_service import CitizenService
from utils.dependencies import get_current_citizen
from config.db import get_db
from models.citizen import Citizen
from utils.govcarpeta_client import GovCarpetaClient

router = APIRouter(prefix="/citizens", tags=["Citizens"])

@router.post("/register", response_model=CitizenResponse)
async def register_citizen(citizen: CitizenCreate, db: Session = Depends(get_db)):

    service = CitizenService(db)

    try:
        citizen_db, access_token = await service.register_citizen(citizen)
        return CitizenResponse(
            id=citizen_db.id,
            name=citizen_db.name,
            email=citizen_db.email,
            civi_email=citizen_db.civi_email,
            access_token=access_token
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=CitizenResponse)
async def login(citizen_login: CitizenLogin, db: Session = Depends(get_db)):

    service = CitizenService(db)
    citizen, access_token = await service.authenticate_citizen(citizen_login.email, citizen_login.password)

    if not citizen:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return CitizenResponse(
        id=citizen.id,
        name=citizen.name,
        email=citizen.email,
        civi_email=citizen.civi_email,
        access_token=access_token
    )

@router.get("/profile", response_model=CitizenProfileResponse)
async def read_profile(current_citizen: Citizen = Depends(get_current_citizen)):
    """
    Obtener el perfil del ciudadano autenticado.
    """
    return current_citizen

@router.delete("/me", status_code=204)
async def delete_my_account(current_citizen: Citizen = Depends(get_current_citizen), db: Session = Depends(get_db)):
    """
    Cierra la cuenta permanentemente en CiviTech (elimina localmente y en GovCarpeta).
    """
    service = CitizenService(db)

    try:
        await service.delete_citizen(current_citizen.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return

@router.delete("/delete", status_code=204)
async def delete_citizen(req: UserIdPayload, db: Session = Depends(get_db)):
    """
    Elimina un ciudadano localmente
    """
    service = CitizenService(db)

    print("INFO: Trying to delete citizen with ID:", req.id, flush=True)

    try:
        await service.delete_citizen_db(req.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return

@router.post("/mark-transferred", status_code=200)
async def mark_transferred(req: UserIdPayload, db: Session = Depends(get_db)):
    citizen = db.query(Citizen).filter(Citizen.id == req.id).first()
    if not citizen:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado")

    citizen.is_transferred = True
    db.commit()
    return {"message": "Ciudadano marcado como transferido"}