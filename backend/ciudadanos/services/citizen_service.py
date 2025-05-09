from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.citizen import Citizen
from schemas.citizen import CitizenCreate
from utils.govcarpeta_client import GovCarpetaClient
from utils.security import hash_password, verify_password
from utils.token_client import get_token
from config.constants import GOVCARPETA_OPERATOR_ID, GOVCARPETA_OPERATOR_NAME

class CitizenService:

    def __init__(self, db: Session):
        self.db = db

    async def register_citizen(self, citizen_data: CitizenCreate):
        # Validar que no exista ya un ciudadano con ese email
        existing_citizen = self.db.query(Citizen).filter(Citizen.email == citizen_data.email).first()

        if existing_citizen:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

        # Validar con GovCarpeta si ya existe el ciudadano
        citizen_exists = await GovCarpetaClient.validate_citizen(citizen_data.id)

        if citizen_exists:
            raise HTTPException(status_code=400, detail="El ciudadano ya está registrado en GovCarpeta")

        # Obtener address si existe, si no, dejarlo como None (se enviará como null)
        address = getattr(citizen_data, "address", None)

        gov_payload = {
            "id": citizen_data.id,
            "name": citizen_data.name,
            "address": address,  # Esto será null si address no existe
            "email": citizen_data.email,
            "operatorId": GOVCARPETA_OPERATOR_ID,
            "operatorName": GOVCARPETA_OPERATOR_NAME
        }

        success = await GovCarpetaClient.register_citizen(gov_payload)
        if not success:
            raise HTTPException(status_code=400, detail="Error al registrar en GovCarpeta")

        # Crear correo único
        civi_email = f"{citizen_data.name.lower().replace(' ', '')}.{citizen_data.id}@carpetacolombia.com"

        # Hashear la contraseña
        hashed_pwd = hash_password(citizen_data.password)

        # Crear ciudadano en base de datos local
        citizen = Citizen(
            id=citizen_data.id,
            name=citizen_data.name,
            email=citizen_data.email,
            civi_email=civi_email,
            hashed_password=hashed_pwd
        )

        self.db.add(citizen)
        self.db.commit()
        self.db.refresh(citizen)

        # Generar token
        access_token = await get_token(citizen.id, citizen.name, citizen.email)

        return citizen, access_token

    async def authenticate_citizen(self, email: str, password: str):
        """
        Verifica las credenciales del ciudadano y genera token si es válido
        """
        citizen = self.db.query(Citizen).filter(Citizen.email == email).first()

        if not citizen:
            return None, None

        if not verify_password(password, citizen.hashed_password):
            return None, None

        # Generar token
        access_token = await get_token(citizen.id, citizen.email)

        return citizen, access_token
    
    async def delete_citizen(self, citizen_id: int):
        """Elimina un ciudadano localmente y en GovCarpeta."""
        citizen = self.db.query(Citizen).filter(Citizen.id == citizen_id).first()
        if not citizen:
            raise Exception("Ciudadano no encontrado")

        # Desvincular en GovCarpeta
        success = await GovCarpetaClient.unregister_citizen(citizen.id)
        if not success:
            raise Exception("No se pudo desligar al ciudadano en GovCarpeta")

        # Borrar de la base local
        self.db.delete(citizen)
        self.db.commit()

    async def delete_citizen_db(self, citizen_id: int):
        """
        Elimina un ciudadano localmente (sin eliminar en GovCarpeta).
        """
        citizen = self.db.query(Citizen).filter(Citizen.id == citizen_id).first()
        if not citizen:
            raise Exception("Ciudadano no encontrado")

        # Borrar de la base local
        self.db.delete(citizen)
        self.db.commit()
        return {"message": "Ciudadano eliminado localmente"}
