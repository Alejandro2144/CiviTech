from interfaces.icitizen_register import ICitizenRegister
from models.citizen_models import CitizenRegistrationRequest
import httpx
from config import OPERATOR_ID, OPERATOR_NAME

class CitizenRegistrar(ICitizenRegister):
    def __init__(self):
        self.base_url = "https://govcarpeta-apis-4905ff3c005b.herokuapp.com"

    async def register_citizen_in_api(self, request: CitizenRegistrationRequest) -> bool:
        url = f"{self.base_url}/apis/registerCitizen"
        payload = {
            "id": request.id_number,
            "name": request.full_name,
            "address": request.address,
            "email": request.email,
            "operatorId": OPERATOR_ID,
            "operatorName": OPERATOR_NAME
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 201:
                    return True
                else:
                    response.raise_for_status()
            except Exception as e:
                raise e
