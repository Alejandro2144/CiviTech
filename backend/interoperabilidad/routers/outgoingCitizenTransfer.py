from fastapi import APIRouter, HTTPException, status
from services.outgoingTransactions import *
# from backend.interoperabilidad.services.outgoingTransactions import *
from constants import GOV_CARPETA_BASEURL
from models import *
from schemas import *
from services import *


citizenTransfer = APIRouter()

@citizenTransfer.post("/outgoingTransferCitizen")
async def outgoingTransferCitizen(req: InitialTransferPayload):
    
    # Obtener la URL del operador externo acá mismo
    
    transferAPIURL = req.transferAPIURL

    # Llamar a API del microservicio de ciudadano para obtener la info del ciudadano.

    citizen = getCitizenInfo()
    
    ## Se debe preparar la información del ciudadano para enviarla al operador externo.
    # {
    #     "id": id,
    #     "citizenName": name,
    #     "citizenEmail": email
    # }
    #
    ## Se debe obtener la lista de documentos del ciudadano para enviarlos al operador externo.
    
    urlDocuments = getCitizenDocuments(citizen.id)
    

    response = sendToExternalOperator(citizen, urlDocuments, transferAPIURL)

    return response



# Obtener la lista de operadores externos activos

@citizenTransfer.get("/getOperators", status_code=status.HTTP_200_OK)
async def getOperators():

    operators = getExternalOperatorsList()

    return operators