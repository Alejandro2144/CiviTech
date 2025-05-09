import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN_MICROSERVICE_URL = os.getenv("TOKEN_MICROSERVICE_URL")

async def get_token(citizen_id: int, citizen_name: str, email: str) -> str:
    payload = {
        "id": citizen_id,
        "name": citizen_name,
        "email": email
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_MICROSERVICE_URL, json=payload)

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Error al generar token")
