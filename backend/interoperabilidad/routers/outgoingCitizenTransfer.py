from fastapi import APIRouter, Depends, status
from services.outgoingTransactions import *
from services.citizenInfo import *
from schemas import *
from services import *
from utils.dependencies import get_current_user

citizenTransfer = APIRouter()

@citizenTransfer.post("/outgoingTransferCitizen")
async def outgoingTransferCitizen(req: InitialTransferPayload, current_user = Depends(get_current_user)):
    
    # Obtener la URL del operador externo acá mismo
    
    transferAPIURL = req.transferAPIURL


    # Llamar a API del microservicio de ciudadano para obtener la info del ciudadano.

    #citizen = getCitizenInfo()

    print("INFO: Citizen data retrieved from citizen microservice:", current_user, flush=True)

    ## 🚨 IMPORTANTE: Desvincular al ciudadano en GovCarpeta (sin eliminar localmente)
    unlinkCitizenInCivitech(current_user['id'])

    # 🚨 Marcar como transferido en microservicio ciudadano
    markCitizenAsTransferred(current_user['id'])

    ## Se debe preparar la información del ciudadano para enviarla al operador externo.
    # {
    #     "id": citizen['id'],
    #     "citizenName": citizen['name'],
    #     "citizenEmail": citizen['email']
    # }
    #
    ## Se debe obtener la lista de documentos del ciudadano para enviarlos al operador externo.

    urlDocumentsUnprepared = getCitizenDocuments(current_user['id'])

    print("INFO: Citizen documents retrieved:", urlDocumentsUnprepared, flush=True)

    urlDocuments = prepareURLDocuments(urlDocumentsUnprepared)

    print("INFO: Citizen documents prepared:", urlDocuments, flush=True)

    print("Current user:", current_user["id"], flush=True)

    response = sendToExternalOperator(current_user, urlDocuments, transferAPIURL)

    print("INFO: Citizen data sent to external operator:", response, flush=True)

# Obtener la lista de operadores externos activos

@citizenTransfer.get("/getOperators", status_code=status.HTTP_200_OK)
async def getOperators():

    operators = getExternalOperatorsList()

    return operators
