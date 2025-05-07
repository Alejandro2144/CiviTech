import json
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from schemas.document_schema import DocumentMetadata
from services.document_service import upload_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
async def upload_document_endpoint(
    file: UploadFile = File(...),
    idCitizen: str = Form(...),
    documentTitle: str = Form(...),
    documentType: Optional[str] = Form("document"),
    isCertified: Optional[bool] = Form(False),
    accessControlList: Optional[str] = Form(None)  # Recibimos como texto (JSON string)
):
    # Leer el archivo
    file_content = await file.read()

    # Aquí haces parsing del string recibido
    access_list = []
    if accessControlList:
        try:
            access_list = json.loads(accessControlList)
        except Exception:
            access_list = []

    # Crear el objeto de metadatos
    metadata = DocumentMetadata(
        idCitizen=idCitizen,
        documentTitle=documentTitle,
        documentType=documentType,
        isCertified=isCertified,
        accessControlList=access_list
    )

    # Subir documento y manejar todo el flujo
    response = await upload_document(file_content, file.filename, metadata)

    return response
