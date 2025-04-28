from abc import ABC, abstractmethod
from models.citizen_models import CitizenRegistrationRequest

class ICitizenRegister(ABC):
    @abstractmethod
    async def register_citizen_in_api(self, request: CitizenRegistrationRequest) -> bool:
        """
        Registra un nuevo ciudadano en la API de Carpeta Ciudadana.
        :param request: Objeto con los datos del ciudadano.
        :return: True si el registro fue exitoso, False en caso contrario.
        """
        pass