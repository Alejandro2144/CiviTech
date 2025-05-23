import json
from fastapi import HTTPException, status
import httpx
from constants import GOV_CARPETA_BASEURL, CIVITECH_CONFIRMATION_API
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

def sendToExternalOperator(citizen, urlDocuments, transferAPIURL):
    
    # Preparar el payload con la información del ciudadano (id, name, email) y los documentos
    payload = {
        "id": citizen['id'],
        "citizenName": citizen['name'],
        "citizenEmail": citizen['email'],
        "urlDocuments": urlDocuments,
        "confirmAPIURL": CIVITECH_CONFIRMATION_API
    }
    # Enviar el payload al operador externo

    '''with httpx.Client() as client:
        try:
            client.request(
            method="POST",
            url=payload['confirmAPIURL'],
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
            )
        except httpx.RequestError as e:
            print(f"Error contactando el microservicio de ciudadanos: {e}", flush=True)
            return
        except httpx.HTTPStatusError as e:
            print(f"Error en la respuesta del microservicio de ciudadanos: {e}", flush=True)
            return
        except Exception as e:
            print(f"Error inesperado: {e}", flush=True)
            return'''

    print("Payload enviado al operador externo:", payload, flush=True)
    
    return payload