from fastapi import HTTPException, status
import httpx
from constants import GOV_CARPETA_BASEURL
from models import *
from schemas import *

# Get the list of active external operators

def getExternalOperatorsList():
    url = f"{GOV_CARPETA_BASEURL}/getOperators"
    try:
        # synchronous HTTP client
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
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

    # Filter only operators with a non-empty transferAPIURL
    filtered = [
        item for item in data
        if item.get("transferAPIURL") and item["transferAPIURL"].strip()
    ]

    return filtered


# Send citizen data to external operator

def sendToExternalOperator(citizen_id: int):

    data = MOCK_CITIZENS.get(citizen_id)

    if not data:
        raise HTTPException(status_code=404, detail="Ciudadano no encontrado")

    # 3.2 Construir el payload
    payload = TransferPayload(id=citizen_id, **data)
    url = f"{GOV_CARPETA_BASEURL}/transferCitizen"
    try:
        # synchronous HTTP client
        with httpx.Client() as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
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

    return data