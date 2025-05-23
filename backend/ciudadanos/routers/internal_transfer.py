from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.citizen import CitizenBase
from models.citizen import Citizen
from utils.govcarpeta_client import GovCarpetaClient
from utils.password_token import generate_set_password_token
from utils.producer import send_citizen_registered
from config.db import get_db
from dotenv import load_dotenv
from config.constants import CIVITECH_BASE_URL

router = APIRouter()

@router.post("/citizens/internal-transfer")
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

    load_dotenv()

    url = f"{CIVITECH_BASE_URL}/set-password?token={token}"

    # Enviar correo al ciudadano
    await send_citizen_registered(citizen.name, citizen.email, url)

    # Notificar a interoperabilidad (para notificaciones)

    print(new_citizen, flush=True)

    return {"message": "Ciudadano pre-registrado y notificado"}
