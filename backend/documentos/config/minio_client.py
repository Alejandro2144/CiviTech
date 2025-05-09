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
