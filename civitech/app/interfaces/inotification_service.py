from abc import ABC, abstractmethod

class INotificationService(ABC):
    @abstractmethod
    def notify_mintic(self, id_number: str, assigned_email: str) -> None:
        """
        Notifica al Ministerio TIC sobre el registro de un nuevo ciudadano.
        :param id_number: Número de identificación del ciudadano.
        :param assigned_email: Correo electrónico asignado al ciudadano.
        :return: None
        """
        pass