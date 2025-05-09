import os
from aio_pika import connect_robust

RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
USER_QUEUE = "user_queue"
DOC_QUEUE  = "document_queue"
ID_USER_QUEUE = "id_user_queue"
UPLOAD_CONFIRM_QUEUE = "upload_confirm_queue"
NOTIFY_QUEUE = "notify_citizen"

async def get_connection():
    return await connect_robust(RABBIT_URL)