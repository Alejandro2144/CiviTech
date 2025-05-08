from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.citizen import CitizenBase
from models.citizen import Citizen
from utils.govcarpeta_client import GovCarpetaClient
from utils.password_token import generate_set_password_token
from utils.producer import send_citizen_registered
from config.db import get_db

router = APIRouter(prefix="/citizens/internal-transfer", tags=["Internal Transfer"])

@router.post("/")
async def receive_citizen(citizen: CitizenBase, db: Session = Depends(get_db)):

    existing = db.query(Citizen).filter(Citizen.id == citizen.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ciudadano ya existe")

    # Validar en GovCarpeta
    is_valid = await GovCarpetaClient.validate_citizen(citizen.id)
    if not is_valid:
        raise HTTPException(status_code=400, detail="El ciudadano no es válido en GovCarpeta")

    # Crear correo único
    civi_email = f"{citizen.name.lower().replace(' ', '')}.{citizen.id}@carpetacolombia.com"

    new_citizen = Citizen(
        id=citizen.id,
        name=citizen.name,
        email=citizen.email,
        civi_email=civi_email,
        hashed_password=None,
        password_set=False
    )

    db.add(new_citizen)
    db.commit()

    # Generar token URL
    token = generate_set_password_token(citizen.id, citizen.email)
    url = f"https://civitech.com/set-password?token={token}"

    # Notificar a interoperabilidad (para notificaciones)
    await send_citizen_registered(citizen.id, citizen.name, citizen.email, url)

    return {"message": "Ciudadano pre-registrado y notificado"}
