import os
import aio_pika
from dotenv import load_dotenv
from config.constants import RABBIT_URL
load_dotenv()

async def get_connection():
    return await aio_pika.connect_robust(RABBIT_URL)
