from interfaces.icitizen_validator import ICitizenValidator
import httpx

class CitizenValidator(ICitizenValidator):
    def __init__(self):
        self.base_url = "https://govcarpeta-apis-4905ff3c005b.herokuapp.com"

    async def validate_citizen_existence(self, id_number: str) -> bool:
        url = f"{self.base_url}/apis/validateCitizen/{id_number}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)

                if response.status_code == 200:
                    # El ciudadano sí existe
                    return True
                elif response.status_code == 204:
                    # El ciudadano no existe
                    return False
                else:
                    # Otro tipo de error
                    response.raise_for_status()

            except Exception as e:
                # Errores de red, de servidor, etc.
                raise e
