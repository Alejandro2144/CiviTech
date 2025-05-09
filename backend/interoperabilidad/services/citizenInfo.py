import json
from fastapi import HTTPException, status
import httpx
from constants import CIUDADANOS_BASE_URL, GOV_CARPETA_BASEURL, OPERATOR_ID, OPERATOR_NAME
from schemas import *

# Get the citizen info from the citizen microservice

def getCitizenInfo():

    url = CIUDADANOS_BASE_URL + "/citizens/profile"

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
    
    documents_api = f"{DOCUMENT_MS_URL}/list/{citizen_id}"

    # llamar a la API del microservicio de documentos para obtener la lista de documentos
    # del ciudadano
    
    try:
        with httpx.Client() as client:
            documents = client.request(
                method="GET",
                url=documents_api
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error contactando Documents: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Documentos devolvió error: {e.response.text}"
        )

    #documents = {"URL1": "https://example.com/doc1", "URL2": "https://example.com/doc2"}  # Mocked response

    return documents

def unlinkCitizenInCivitech(citizen_id: int):
    url = f"{GOV_CARPETA_BASEURL}/unregisterCitizen"

    payload = {
        "id": citizen_id,
        "operatorId": OPERATOR_ID,
        "operatorName": OPERATOR_NAME
    }

    try:
        with httpx.Client() as client:
            response = client.request(
                method="DELETE",
                url=url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error contactando GovCarpeta: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GovCarpeta devolvió error: {e.response.text}"
        )

def markCitizenAsTransferred(citizen_id: int):
    url = f"{CIUDADANOS_BASE_URL}/citizens/mark-transferred"
    payload = {"id": citizen_id}

    try:
        with httpx.Client() as client:
            response = client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"No se pudo contactar el microservicio de ciudadanos: {e}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error al marcar como transferido: {e.response.text}"
        )