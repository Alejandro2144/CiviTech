from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.set_password import SetPasswordRequest, SetPasswordResponse
from utils.password_token import verify_set_password_token
from utils.security import hash_password
from utils.token_client import get_token
from models.citizen import Citizen
from config.db import get_db

router = APIRouter(prefix="/citizens", tags=["Citizens"])

@router.post("/set-password", response_model=SetPasswordResponse)
async def set_password(data: SetPasswordRequest, db: Session = Depends(get_db)):

    payload = verify_set_password_token(data.token)

    if not payload:
        raise HTTPException(status_code=400, detail="Token inválido o expirado.")

    citizen_id = payload.get("id")
    email = payload.get("email")

    citizen = db.query(Citizen).filter(Citizen.id == citizen_id, Citizen.email == email).first()

    if not citizen:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado.")

    if citizen.password_set:
        raise HTTPException(status_code=400, detail="La contraseña ya fue asignada.")

    # Asignar nueva contraseña
    citizen.hashed_password = hash_password(data.password)
    citizen.password_set = True

    db.commit()

    # Generar token de acceso
    access_token = await get_token(citizen.id, citizen.name, citizen.email)

    return SetPasswordResponse(access_token=access_token)
