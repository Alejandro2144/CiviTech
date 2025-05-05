from sqlalchemy.orm import Session
from ..models.citizen import Citizen
from ..schemas.citizen import CitizenCreate
from ..utils.govcarpeta_client import GovCarpetaClient
from ..utils.security import hash_password

class CitizenService:

    def __init__(self, db: Session):
        self.db = db

    async def register_citizen(self, citizen_data: CitizenCreate):

        # Validar con GovCarpeta si ya existe
        citizen_exists = await GovCarpetaClient.validate_citizen(citizen_data.id)

        if citizen_exists:
            raise Exception("El ciudadano ya está registrado en GovCarpeta")

        # Registrar en GovCarpeta
        gov_payload = {
            "id": citizen_data.id,
            "name": citizen_data.name,
            "address": citizen_data.address,
            "email": citizen_data.email,
            "operatorId": "operador_civitech_id",
            "operatorName": "Operador CiviTech"
        }

        success = await GovCarpetaClient.register_citizen(gov_payload)
        if not success:
            raise Exception("Error al registrar en GovCarpeta")

        # Crear correo único
        civi_email = f"{citizen_data.name.lower().replace(' ', '')}.{citizen_data.id}@carpetacolombia.com"

        # Hashear contraseña
        hashed_pwd = hash_password(citizen_data.password)

        # Guardar en base de datos local
        citizen = Citizen(
            id=citizen_data.id,
            name=citizen_data.name,
            address=citizen_data.address,
            email=citizen_data.email,
            civi_email=civi_email,
            hashed_password=hashed_pwd
        )

        self.db.add(citizen)
        self.db.commit()
        self.db.refresh(citizen)

        return citizen
