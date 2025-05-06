from config.minio_client import get_minio_client
from schemas.document_schema import DocumentMetadata
import uuid
import io

bucket_name = "documents"

def upload_document(file_data: bytes, filename: str, metadata: DocumentMetadata):
    client = get_minio_client()

    # Asegurarse que el bucket exista
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Crear nombre único para evitar conflictos
    unique_filename = f"{uuid.uuid4()}_{filename}"

    # Convertir bytes a un objeto file-like con método read()
    file_data_io = io.BytesIO(file_data)

    # Subir archivo
    client.put_object(
        bucket_name=bucket_name,
        object_name=unique_filename,
        data=file_data_io,
        length=len(file_data),
        metadata={
            "x-amz-meta-user_id": metadata.user_id,
            "x-amz-meta-document_type": metadata.document_type,
            "x-amz-meta-description": metadata.description or ""
        }
    )

    return unique_filename
