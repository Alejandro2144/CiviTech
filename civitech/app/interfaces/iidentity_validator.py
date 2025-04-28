from abc import ABC, abstractmethod
from models.citizen_models import CitizenRegistrationRequest

class IIdentityValidator(ABC):
    @abstractmethod
    def validate_identity(self, request: CitizenRegistrationRequest) -> bool:
        """
        Valida la identidad del ciudadano a partir de los datos del formulario.
        :param request: Objeto con los datos del ciudadano.
        :return: True si la identidad es validada, False en caso contrario.
        """
        pass
