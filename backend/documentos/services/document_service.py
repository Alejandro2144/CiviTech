from config.minio_client import get_minio_client
from config.minio_client import generate_presigned_url
from utils.govcarpeta_client import GovCarpetaClient
from schemas.document_schema import DocumentMetadata
import io
import json

bucket_name = "documents"

async def upload_document(file_data: bytes, original_filename: str, metadata: DocumentMetadata):
    client = get_minio_client()

    # Asegurarnos que el bucket existe
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Generar nombre final
    final_filename = f"{metadata.idDocument}_{original_filename}"

    # Generar la URL firmada para el acceso al documento
    signed_url = generate_presigned_url(
        bucket_name=bucket_name,
        object_name=final_filename
    )

    # Actualizar el metadata.urlDocument con el URL firmado
    metadata.urlDocument = signed_url

    # Autenticar en GovCarpeta
    metadata_dict = metadata.model_dump()
    auth_status, auth_date = await GovCarpetaClient.authenticate_document(metadata_dict)

    metadata.authenticationStatus = auth_status
    metadata.authenticationDate = auth_date

    # Convertir bytes a un objeto file-like con método read()
    file_data_io = io.BytesIO(file_data)

    # Subir el archivo a MinIO
    client.put_object(
        bucket_name=bucket_name,
        object_name=final_filename,
        data=file_data_io,
        length=len(file_data),
        metadata={
            "x-amz-meta-idCitizen": metadata.idCitizen,
            "x-amz-meta-documentTitle": metadata.documentTitle,
            "x-amz-meta-documentType": metadata.documentType,
            "x-amz-meta-uploadDate": metadata.uploadDate.isoformat(),
            "x-amz-meta-isCertified": str(metadata.isCertified),
            "x-amz-meta-authenticationStatus": metadata.authenticationStatus,
            "x-amz-meta-accessControlList": ",".join(metadata.accessControlList or [])
        }
    )

    serializable_metadata = {
        "idDocument": str(metadata.idDocument),
        "idCitizen": metadata.idCitizen,
        "documentTitle": metadata.documentTitle,
        "urlDocument": metadata.urlDocument,
        "uploadDate": metadata.uploadDate.isoformat() if metadata.uploadDate else None,
        "documentType": metadata.documentType,
        "isCertified": metadata.isCertified,
        "authenticationStatus": metadata.authenticationStatus,
        "authenticationDate": metadata.authenticationDate.isoformat() if metadata.authenticationDate else None,
        "accessControlList": metadata.accessControlList if metadata.accessControlList else []
    }

    return {
        "message": "Documento cargado y autenticado correctamente.",
        "metadata": serializable_metadata
    }