from abc import ABC, abstractmethod

class ICitizenValidator(ABC):
    @abstractmethod
    async def validate_citizen_existence(self, id_number: str) -> bool:
        """
        Verifica si un ciudadano ya está registrado en el sistema.
        :param id_number: Número de identificación del ciudadano.
        :return: True si existe, False si no existe.
        """
        pass