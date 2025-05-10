from datetime import timedelta
import mimetypes
from fastapi import HTTPException
from services.notify_action_service import publish_notification_message
from config.minio_client import get_minio_client
from utils.govcarpeta_client import GovCarpetaClient
from schemas.document_schema import DocumentMetadata
import io, os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bucket_name = "documents"

async def upload_document(file_data: bytes, original_filename: str, metadata: DocumentMetadata, user: dict, force_update: bool = False):
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
    signed_url = generate_signed_url(final_filename, expiry_seconds=3600)
    metadata.urlDocument = signed_url

    # Autenticar contra GovCarpeta
    await handle_authentication(metadata)

    # Borrar el objeto anterior
    client.remove_object(bucket_name, final_filename)

    # Volver a subir metadata si cambia por autenticación
    upload_to_minio(client, bucket_name, final_filename, file_data, prepare_object_metadata(metadata))

    await publish_notification_message(
        CitizenName=user["name"],
        CitizenEmail=user["email"],
        fileAction="carga",
        fileName=final_filename
    )

    return {
        "message": "Documento cargado o actualizado y autenticado correctamente.",
        "metadata": metadata
    }

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
                # Generar URL firmada para este documento
                signed_url = generate_signed_url(obj.object_name, expiry_seconds=3600)

                # Construir respuesta con la URL firmada incluida
                document_info = {
                    "objectName": obj.object_name,
                    "documentTitle": metadata.get("x-amz-meta-documentTitle", ""),
                    "documentType": metadata.get("x-amz-meta-documentType", ""),
                    "uploadDate": metadata.get("x-amz-meta-uploadDate", ""),
                    "isCertified": metadata.get("x-amz-meta-isCertified", "false").lower() == "true",
                    "urlDocument": signed_url,
                    "authenticationStatus": metadata.get("x-amz-meta-authenticationStatus", "pending")
                }
                found_documents.append(document_info)
        except Exception as e:
            print(f"[ERROR] No se pudo leer metadata de {obj.object_name}: {e}")
            continue

    return found_documents

async def delete_document(object_name: str, user: dict = None):
    client = get_minio_client()
    try:
        # Obtener metadata del objeto
        stat = client.stat_object(bucket_name="documents", object_name=object_name)
        metadata = stat.metadata
        title = metadata.get("x-amz-meta-documentTitle", object_name)

        # Eliminar el documento               
        client.remove_object(bucket_name="documents", object_name=object_name)

        if user:
            await publish_notification_message(
                CitizenName=user["name"],
                CitizenEmail=user["email"],
                fileAction="eliminado",
                fileName=title
            )
        return {"message": f"Documento '{object_name}' eliminado correctamente."}
    
    except Exception as e:
        print(f"[ERROR] Error eliminando documento: {e}")
        raise HTTPException(status_code=500, detail="Error eliminando documento. Reintente más tarde.")
    
async def delete_folder_by_citizen(idCitizen: str):
    client = get_minio_client()

    if not client.bucket_exists(bucket_name):
        raise HTTPException(status_code=404, detail="Bucket de documentos no encontrado.")

    objects_to_delete = []
    objects = client.list_objects(bucket_name, recursive=True)

    for obj in objects:
        try:
            info = client.stat_object(bucket_name, obj.object_name)
            metadata = info.metadata

            if metadata.get("x-amz-meta-idCitizen") == idCitizen:
                objects_to_delete.append(obj.object_name)
        except Exception as e:
            print(f"[ERROR] Error leyendo metadata de {obj.object_name}: {e}")
            continue

    if not objects_to_delete:
        return {"message": "No se encontraron documentos para este ciudadano."}

    # Eliminar cada objeto encontrado
    for object_name in objects_to_delete:
        try:
            client.remove_object(bucket_name, object_name)
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar {object_name}: {e}")

    return {"message": f"La Carpeta del ciudadano {idCitizen} fue eliminada correctamente."}


def generate_signed_url(object_name: str, expiry_seconds: int = 3600, disposition: str = "inline") -> str:
    """
    Genera una URL firmada para visualizar el documento.
    """
    client = get_minio_client()

    # Detectar el Content-Type basado en la extensión
    content_type, _ = mimetypes.guess_type(object_name)

    # Si no logra adivinar, por defecto usamos application/octet-stream
    if not content_type:
        content_type = "application/octet-stream"

    # Agregar headers
    response_headers = {
        "response-content-disposition": f'{disposition}; filename="{object_name}"',
        "response-content-type": content_type
    }

    url = client.presigned_get_object(
        bucket_name=bucket_name,
        object_name=object_name,
        expires=timedelta(seconds=expiry_seconds),
        response_headers=response_headers
    )
    return url

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
    auth_status, auth_date = await GovCarpetaClient.authenticate_document(metadata.model_dump())
    metadata.authenticationStatus = auth_status
    metadata.authenticationDate = auth_date

