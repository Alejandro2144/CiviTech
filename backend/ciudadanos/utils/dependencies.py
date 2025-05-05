import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from config.db import get_db
from models.citizen import Citizen
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.token import decode_token

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

bearer_scheme = HTTPBearer()

async def get_current_citizen(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Citizen:
    
    token = credentials.credentials

    payload = decode_token(token)
    citizen_id = payload.get("id")

    citizen = db.query(Citizen).filter(Citizen.id == citizen_id).first()

    if not citizen:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado")

    return citizen
