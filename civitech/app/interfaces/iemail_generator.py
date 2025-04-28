from abc import ABC, abstractmethod

class IEmailGenerator(ABC):
    @abstractmethod
    def generate_unique_email(self, full_name: str, id_number: str) -> str:
        """
        Genera un correo electrónico único basado en el nombre completo y el número de identificación.
        :param full_name: Nombre completo del ciudadano.
        :param id_number: Número de identificación del ciudadano.
        :return: Correo electrónico generado.
        """
        pass