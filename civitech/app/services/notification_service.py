from interfaces.inotification_service import INotificationService

class NotificationService(INotificationService):
    def notify_mintic(self, id_number: str, assigned_email: str) -> None:
        """
        Mock de notificación al Ministerio TIC.
        En una implementación real, se enviaría una solicitud HTTP a un endpoint oficial.
        """
        print(f"[Mock] Notificando al Ministerio TIC: Ciudadano {id_number} registrado con correo {assigned_email}")
        # En una versión real: aquí iría una llamada a un servicio externo
        return