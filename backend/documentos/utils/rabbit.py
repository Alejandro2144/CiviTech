import os
import aio_pika

RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

async def get_connection():
    return await aio_pika.connect_robust(RABBIT_URL)
