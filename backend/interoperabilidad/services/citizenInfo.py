from fastapi import HTTPException, status
import httpx
from constants import GOV_CARPETA_BASEURL
from models import *
from schemas import *

# Get the citizen info from the citizen microservice

def getCitizenInfo():

    url = "http://citizen-microservice:8000/citizen"
    
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