from datetime import datetime, timezone
import io
import aiohttp
import mimetypes
from config.minio_client import get_minio_client
from services.confirm_service import publish_confirmation_message
from urllib.parse import urlparse, unquote

bucket_name = "documents"

async def download_file(url: str) -> bytes:
    """
    Descarga un archivo desde una URL pública.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"No se pudo descargar el archivo desde {url}. Status: {response.status}")
            return await response.read()

async def process_transfer_message(payload: dict):
    """
    Procesa un mensaje de transferencia:
    - Descarga los documentos
    - Los almacena en el bucket
    - Publica confirmación
    """
    client = get_minio_client()

    id_citizen = str(payload.get("id"))
    url_documents = payload.get("urlDocuments", {})
    confirm_api = payload.get("confirmAPI")  # Guardamos pero aún no usamos en esta versión

    if not id_citizen or not url_documents:
        raise Exception("Payload inválido: falta id o urlDocuments")

    saved_documents = []

    for doc_key, url_list in url_documents.items():
        for url in url_list:
            try:
                # Descargar el archivo desde la URL
                file_data = await download_file(url)
                
            # Paso 1: Extraer el path limpio de la URL
                parsed_url = urlparse(url)
                path = parsed_url.path  # /documents/filename.jpg
                filename = unquote(path.split("/")[-1])  # filename.jpg (sin %22, etc.)

                # Paso 2: Intentar extraer la extensión real
                extension = ""
                if "." in filename:
                    extension = filename.split(".")[-1].split("?")[0].split("%")[0].lower()

                # Paso 3: Si no logramos detectar extensión válida, usar MIME como respaldo
                if not extension or extension not in ["jpg", "jpeg", "png", "pdf", "doc", "docx"]:
                    content_type, _ = mimetypes.guess_type(filename)
                    if content_type and "/" in content_type:
                        subtype = content_type.split("/")[1]
                        extension = {
                            "jpeg": "jpg",
                            "png": "png",
                            "pdf": "pdf",
                            "msword": "doc",
                            "vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
                        }.get(subtype, "bin")

                # Paso 4: Asegurar valor por defecto
                if not extension:
                    extension = "bin"

                object_name = f"{id_citizen}_{doc_key}.{extension}"
                current_time = datetime.now(timezone.utc).isoformat()

                metadata = {
                    "x-amz-meta-idCitizen": id_citizen,
                    "x-amz-meta-documentTitle": doc_key,
                    "x-amz-meta-documentType": "document",
                    "x-amz-meta-uploadDate": current_time,
                    "x-amz-meta-isCertified": "true",  # Suponemos que vienen certificados
                    "x-amz-meta-authenticationStatus": "authenticated"
                }

                file_data_io = io.BytesIO(file_data)

                client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    data=file_data_io,
                    length=len(file_data),
                    metadata=metadata
                )

                saved_documents.append(object_name)
                print(f"[DEBUG] Documento {object_name} guardado exitosamente.")

            except Exception as e:
                print(f"[ERROR] Error procesando documento {url}: {e}")

    if not saved_documents:
        raise Exception("No se pudo guardar ningún documento.")
    
    # Publicar confirmación después de guardar exitosamente los documentos
    await publish_confirmation_message(
    id_citizen=id_citizen,
    confirm_api=confirm_api,
    status="1"
)