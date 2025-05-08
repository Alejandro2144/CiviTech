import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN_MICROSERVICE_URL = os.getenv("TOKEN_MICROSERVICE_URL")

async def get_token_for_interoperabilidad():
    payload = {
        "id": 0,
        "email": "interoperabilidad@civitech.com"  
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_MICROSERVICE_URL, json=payload)

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Error al generar token para interoperabilidad")
