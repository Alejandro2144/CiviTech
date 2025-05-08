import json
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from schemas.document_schema import DocumentMetadata
from services.document_service import upload_document
from services.document_service import list_documents_by_citizen
from services.document_service import generate_signed_url
from services.document_service import delete_document

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
    accessControlList: Optional[str] = Form(None),
    forceUpdate: bool = Form(default=False)
):
    """
    Sube un documento a GovCarpeta y lo autentica.
    """
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
    response = await upload_document(file_content, file.filename, metadata,force_update=forceUpdate)

    return response

@router.get("/list/{idCitizen}")
async def list_documents(idCitizen: str):
    """
    Lista los documentos pertenecientes a un ciudadano específico.
    """
    documents = await list_documents_by_citizen(idCitizen)
    if not documents:
        return {"message": "No tienes documentos cargados."}
    return {"documents": documents}

@router.get("/view/{object_name}")
async def view_document(object_name: str):
    """
    Genera una URL firmada para visualizar un documento específico.
    """
    view_url = generate_signed_url(object_name)
    return {"viewUrl": view_url}

@router.get("/download/{object_name}")
async def download_document(object_name: str):
    """
    Genera una URL firmada para descargar un documento específico.
    """
    download_url = generate_signed_url(object_name, disposition="attachment")
    return {"downloadUrl": download_url}

@router.delete("/delete/{object_name}")
async def delete_document_endpoint(object_name: str):
    """
    Elimina un documento específico del bucket.
    """
    response = await delete_document(object_name)
    return response