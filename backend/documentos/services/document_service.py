from fastapi import HTTPException
from config.minio_client import get_minio_client
from config.minio_client import generate_presigned_url
from utils.govcarpeta_client import GovCarpetaClient
from schemas.document_schema import DocumentMetadata
import io
import json

bucket_name = "documents"

async def upload_document(file_data: bytes, original_filename: str, metadata: DocumentMetadata, force_update: bool = False):
    client = get_minio_client()
    ensure_bucket_exists(client, bucket_name="documents")

    final_filename = f"{metadata.idDocument}_{original_filename}"

    # Verificar si ya existe
    existing_object = find_existing_document(client, metadata.idCitizen, metadata.documentTitle, metadata.documentType)

    if existing_object and not force_update:
        raise HTTPException(
            status_code=409,
            detail="Documento ya existe. ¿Desea actualizarlo?"
        )

    if existing_object:
        final_filename = existing_object
        try:
            stat = client.stat_object(bucket_name, final_filename)
            existing_metadata = stat.metadata
            previous_idDocument = existing_metadata.get("x-amz-meta-iddocument")
            if previous_idDocument:
                metadata.idDocument = previous_idDocument
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error obteniendo metadata previa.")
    else:
        final_filename = f"{metadata.idDocument}_{original_filename}"

    #Subir archivo inicialmente a MinIO (sin firmarlo aún)
    upload_to_minio(client, bucket_name, final_filename, file_data, prepare_object_metadata(metadata))

    # Generar URL firmada
    signed_url = generate_presigned_url(bucket_name="documents", object_name=final_filename)
    metadata.urlDocument = signed_url

    # Autenticar contra GovCarpeta
    await handle_authentication(metadata)

    # Borrar el objeto anterior
    client.remove_object(bucket_name, final_filename)

    # Volver a subir metadata si cambia por autenticación
    upload_to_minio(client, bucket_name, final_filename, file_data, prepare_object_metadata(metadata))

    return {
        "message": "Documento cargado o actualizado y autenticado correctamente.",
        "metadata": metadata
    }

def ensure_bucket_exists(client, bucket_name):
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

def find_existing_document(client, idCitizen: str, documentTitle: str, documentType: str):
    """
    Busca si existe un documento para el ciudadano con título y tipo.
    """
    try:
        objects = client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            stat = client.stat_object(bucket_name, obj.object_name)
            meta = stat.metadata
            if (meta.get("x-amz-meta-idCitizen") == idCitizen and
                meta.get("x-amz-meta-documentTitle") == documentTitle and
                meta.get("x-amz-meta-documentType") == documentType):
                return obj.object_name
        return None
    except Exception as e:
        return None

def prepare_object_metadata(metadata: DocumentMetadata) -> dict:
    return {
        "x-amz-meta-idDocument": metadata.idDocument,
        "x-amz-meta-idCitizen": metadata.idCitizen,
        "x-amz-meta-documentTitle": metadata.documentTitle,
        "x-amz-meta-documentType": metadata.documentType,
        "x-amz-meta-uploadDate": metadata.uploadDate.isoformat(),
        "x-amz-meta-isCertified": str(metadata.isCertified),
        "x-amz-meta-authenticationStatus": metadata.authenticationStatus,
        "x-amz-meta-accessControlList": ",".join(metadata.accessControlList or [])
    }

def upload_to_minio(client, bucket_name, object_name, file_data: bytes, metadata: dict):
    file_data_io = io.BytesIO(file_data)
    client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=file_data_io,
        length=len(file_data),
        metadata=metadata
    )

async def handle_authentication(metadata: DocumentMetadata):
    auth_status, auth_date = await GovCarpetaClient.authenticate_document(metadata.dict())
    metadata.authenticationStatus = auth_status
    metadata.authenticationDate = auth_date

async def list_documents_by_citizen(idCitizen: str):
    client = get_minio_client()

    if not client.bucket_exists(bucket_name):
        return []

    found_documents = []

    # Listar todos los objetos en el bucket
    objects = client.list_objects(bucket_name, recursive=True)

    for obj in objects:
        # Para cada objeto, obtener su metadata
        try:
            info = client.stat_object(bucket_name, obj.object_name)
            metadata = info.metadata

            if metadata.get("x-amz-meta-idCitizen") == idCitizen:
                # Construir respuesta parcial
                document_info = {
                    "objectName": obj.object_name,
                    "documentTitle": metadata.get("x-amz-meta-documentTitle", ""),
                    "documentType": metadata.get("x-amz-meta-documentType", ""),
                    "uploadDate": metadata.get("x-amz-meta-uploadDate", ""),
                    "isCertified": metadata.get("x-amz-meta-isCertified", "false") == "true"
                }
                found_documents.append(document_info)
        except Exception as e:
            print(f"[ERROR] No se pudo leer metadata de {obj.object_name}: {e}")
            continue

    return found_documents