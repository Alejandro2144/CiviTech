import httpx
from config.constants import GOVCARPETA_BASE_URL, GOVCARPETA_OPERATOR_ID, GOVCARPETA_OPERATOR_NAME

class GovCarpetaClient:

    @staticmethod
    async def validate_citizen(citizen_id: str) -> bool:
        """
        Verifica si un ciudadano está registrado en GovCarpeta.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GOVCARPETA_BASE_URL}/apis/validateCitizen/{citizen_id}")

            if response.status_code == 200:
                return True  # El ciudadano existe
            elif response.status_code == 204:
                return False  # No existe
            else:
                raise Exception(f"Error consultando GovCarpeta -> {response.status_code} {response.text}")

    @staticmethod
    async def register_citizen(citizen_data: dict) -> bool:
        """
        Registra un ciudadano en GovCarpeta.
        """
        async with httpx.AsyncClient() as client:
            payload = {
                "id": str(citizen_data["id"]),
                "name": citizen_data["name"],
                "address": citizen_data["address"],
                "email": citizen_data["email"],
                "operatorId": GOVCARPETA_OPERATOR_ID,
                "operatorName": GOVCARPETA_OPERATOR_NAME
            }

            response = await client.post(f"{GOVCARPETA_BASE_URL}/apis/registerCitizen", json=payload)

            if response.status_code == 201:
                return True
            else:
                return False

    @staticmethod
    async def unregister_citizen(citizen_id: str) -> bool:
        """Desvincula un ciudadano en GovCarpeta."""
        payload = {
            "id": citizen_id,
            "operatorId": GOVCARPETA_OPERATOR_ID,
            "operatorName": GOVCARPETA_OPERATOR_NAME
        }

        async with httpx.AsyncClient() as client:
            response = await client.request(
                "DELETE", 
                f"{GOVCARPETA_BASE_URL}/apis/unregisterCitizen",
                json=payload
            )
            return response.status_code in (200, 201, 204)

