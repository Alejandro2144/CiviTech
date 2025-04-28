from interfaces.iemail_generator import IEmailGenerator

class EmailGenerator(IEmailGenerator):
    def generate_unique_email(self, full_name: str, id_number: str) -> str:
        """
        Genera un correo electrónico único basado en el nombre completo y el número de identificación.
        """
        # Limpiar el nombre (minúsculas, sin espacios extras)
        clean_name = full_name.strip().lower().replace(" ", ".")
        
        # Construir el correo electrónico
        email = f"{clean_name}.{id_number}@civitech.com"
        return email