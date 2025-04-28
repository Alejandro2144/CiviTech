from interfaces.iidentity_validator import IIdentityValidator
from models.citizen_models import CitizenRegistrationRequest

class IdentityValidator(IIdentityValidator):
    def validate_identity(self, request: CitizenRegistrationRequest) -> bool:
        """
        Mock de validación de identidad. 
        En una implementación real, aquí se consultaría la Registraduría.
        """
        # Por ahora, simplemente aceptamos que cualquier ID que sea numérico y tenga más de 5 dígitos es válido.
        if request.id_number.isdigit() and len(request.id_number) >= 6:
            return True
        return False