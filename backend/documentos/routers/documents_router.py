from fastapi import APIRouter, UploadFile, File, Form
from schemas.document_schema import DocumentMetadata
from services.document_service import upload_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
async def upload_document_endpoint(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    document_type: str = Form(...),
    description: str = Form(None)
):
    file_content = await file.read()

    metadata = DocumentMetadata(
        user_id=user_id,
        document_type=document_type,
        description=description
    )

    saved_filename = upload_document(file_content, file.filename, metadata)

    return {"message": "Document uploaded successfully", "filename": saved_filename}
