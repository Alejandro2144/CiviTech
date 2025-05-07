from fastapi import APIRouter, HTTPException, status
from services.externalOperators import *
from constants import GOV_CARPETA_BASEURL
from models import *
from schemas import *
from services import *


citizenTransfer = APIRouter()

@citizenTransfer.post("/transfer-citizen/{citizen_id}", response_model=TransferPayload)
async def transfer_citizen(citizen_id: int):
    
    response = sendToExternalOperator(citizen_id)

    return response



# Obtener la lista de operadores externos activos

@citizenTransfer.get("/getOperators", status_code=status.HTTP_200_OK)
async def getOperators():

    operators = getExternalOperatorsList()

    return operators