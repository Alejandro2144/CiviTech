from fastapi import APIRouter, HTTPException, status
from services.outgoingTransactions import *
from services.citizenInfo import *
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

    citizen = await getCitizenInfo()

    ## 🚨 IMPORTANTE: Desvincular al ciudadano en GovCarpeta (sin eliminar localmente)
    unlinkCitizenInCivitech(citizen['id'])

    ## Se debe preparar la información del ciudadano para enviarla al operador externo.
    # {
    #     "id": citizen['id'],
    #     "citizenName": citizen['name'],
    #     "citizenEmail": citizen['email']
    # }
    #
    ## Se debe obtener la lista de documentos del ciudadano para enviarlos al operador externo.

    urlDocuments = getCitizenDocuments(citizen['id'])

    response = sendToExternalOperator(citizen, urlDocuments, transferAPIURL)

    return response

# Obtener la lista de operadores externos activos

@citizenTransfer.get("/getOperators", status_code=status.HTTP_200_OK)
async def getOperators():

    operators = getExternalOperatorsList()

    return operators
