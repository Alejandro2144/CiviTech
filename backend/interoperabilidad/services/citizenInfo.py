from fastapi import HTTPException, status
import httpx
from constants import GOV_CARPETA_BASEURL, CIUDADANOS_BASE_URL
from models import *
from schemas import *
import asyncio
from utils.token_client import get_token_for_interoperabilidad

async def getCitizenInfo():
    url = f"{CIUDADANOS_BASE_URL}/citizens/profile"

    token = await get_token_for_interoperabilidad()  # 🚨 Usamos await, no asyncio.run

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            data = response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Error contacting upstream service: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Upstream service returned error: {e.response.text}")

    return data


def getCitizenDocuments(citizen_id: int):
    url = f"/citizen/{citizen_id}/documents"
    
    try:
        # synchronous HTTP client
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            documents = response.json()
    except httpx.RequestError as e:
        # network or connection error
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error contacting upstream service: {e}"
        )
    except httpx.HTTPStatusError as e:
        # non-2xx status codes
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Upstream service returned error: {e.response.text}"
        )

    return documents

def unlinkCitizenInCivitech(citizen_id: int):

    url = f"{CIUDADANOS_BASE_URL}/citizens/{citizen_id}/unlink"

    try:
        with httpx.Client() as client:
            response = client.post(url)
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error contactando ciudadanos: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ciudadanos devolvió error: {e.response.text}"
        )

