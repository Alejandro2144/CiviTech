import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from config.constants import AUTH_VALIDATE_URL

load_dotenv()

#AUTH_VALIDATE_URL = os.getenv("AUTH_VALIDATE_URL")

async def validate_token_remote(token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(AUTH_VALIDATE_URL, headers=headers)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=403, detail="Token inválido o expirado")
