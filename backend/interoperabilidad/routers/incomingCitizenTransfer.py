from fastapi import APIRouter, HTTPException, status
from services.outgoingTransactions import *
from schemas import *
from services import *

citizenReceiving = APIRouter()

## This endpoint is called by the user to start the transfer process.

@citizenReceiving.post("/transferCitizen")
async def incomingTransferCitizen(req: TransferPayload):
    await publishUserTransferMessages(req)
    return {"status": "messages (citizen transfer) published by interoperability"}


## This endpoint is called by the documents microservice to confirm
## the correct upload of the documents from the incoming citizen.

@citizenReceiving.post("/confirmTransfer")
async def confirmTransfer(req: confirmTransferPayload):
    """
    Confirm the transfer of a citizen to an external operator.
    """
    # Call the external operator's API to confirm the transfer
    url = req.confirmAPIURL
    
    payload = {
        "id": req.id,
        "req_status": req.req_status
    }

    payload_json = json.dumps(payload)

    try:
        # synchronous HTTP client
        with httpx.Client() as client:
            response = client.post(url, json=payload_json)
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

## This endpoint is called by the external operator to confirm the correct 
## receive of the citizen transfer and documents upload.

@citizenReceiving.post("/transferCitizenConfirm")
async def transferCitizenConfirm(req: ConfirmPayload):
    await publishUserIDConfirmationMessages(req)
    return {"status": "messages (user id) published by interoperability"}

    
