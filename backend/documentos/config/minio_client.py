from minio import Minio
import os
from datetime import timedelta

def get_minio_client():
    client = Minio(
        endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "admin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "admin123"),
        secure=False  # En local trabajamos sin HTTPS
    )
    return client

def generate_presigned_url(bucket_name: str, object_name: str, expiry: int = 3600):
    """
    Genera una URL firmada para acceder a un objeto privado en MinIO.

    :param bucket_name: Nombre del bucket.
    :param object_name: Nombre del archivo.
    :param expiry: Tiempo de expiración en segundos (por defecto 1 hora).
    :return: URL firmada como string.
    """

    minio_client = get_minio_client()

    url = minio_client.presigned_get_object(
        bucket_name=bucket_name,
        object_name=object_name,
        expires=timedelta(seconds=expiry)
    )

    return url
