from fastapi import APIRouter, HTTPException, status
from services.externalOperators import *
from constants import GOV_CARPETA_BASEURL
from models import *
from schemas import *
from services import *


citizenReceiving = APIRouter()

@citizenReceiving.post("/transferCitizen")
async def transfer_citizen(req: TransferPayload):
    await publish_transfer_messages(req)
    return {"status": "messages published by interoperability"}
