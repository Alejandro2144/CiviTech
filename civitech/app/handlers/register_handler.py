from fastapi import Depends, HTTPException
from models.citizen_models import CitizenRegistrationRequest, CitizenRegistrationResponse

from providers.citizen_provider import get_citizen_validator
from providers.identity_provider import get_identity_validator
from providers.register_provider import get_citizen_register
from providers.email_provider import get_email_generator
from providers.notification_provider import get_notification_service

class RegisterCitizenHandler:
    def __init__(
        self,
        citizen_validator = Depends(get_citizen_validator),
        identity_validator = Depends(get_identity_validator),
        citizen_register = Depends(get_citizen_register),
        email_generator = Depends(get_email_generator),
        notification_service = Depends(get_notification_service)
    ):
        self.citizen_validator = citizen_validator
        self.identity_validator = identity_validator
        self.citizen_register = citizen_register
        self.email_generator = email_generator
        self.notification_service = notification_service

    async def handle(self, request: CitizenRegistrationRequest) -> CitizenRegistrationResponse:
        # 1. Validar si el ciudadano ya existe
        exists = await self.citizen_validator.validate_citizen_existence(request.id_number)
        if exists:
            raise HTTPException(status_code=400, detail="El ciudadano ya está registrado en otro operador.")

        # 2. Validar identidad
        valid_identity = self.identity_validator.validate_identity(request)
        if not valid_identity:
            raise HTTPException(status_code=400, detail="Identidad no validada en Registraduría.")

        # 3. Registrar ciudadano en Carpeta
        success = await self.citizen_register.register_citizen_in_api(request)
        if not success:
            raise HTTPException(status_code=500, detail="Error registrando ciudadano en Carpeta Ciudadana.")

        # 4. Generar correo único
        assigned_email = self.email_generator.generate_unique_email(request.full_name, request.id_number)

        # 5. Notificar MinTIC
        self.notification_service.notify_mintic(request.id_number, assigned_email)

        return CitizenRegistrationResponse(
            message="Registro exitoso",
            assigned_email=assigned_email
        )
