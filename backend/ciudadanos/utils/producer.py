import json
import aio_pika
from aio_pika import connect_robust
import os
from dotenv import load_dotenv
from config.constants import RABBIT_URL, NOTIFY_QUEUE
load_dotenv()

async def send_citizen_registered(id, name, email, url):
    conn = await connect_robust(RABBIT_URL)
    chan = await conn.channel()

    await chan.declare_queue(NOTIFY_QUEUE, durable=True)

    payload = json.dumps({
        "id": id,
        "name": name,
        "email": email,
        "set_password_url": url
    }).encode()

    print("🚀 Enviando a notify_citizen:", payload)

    await chan.default_exchange.publish(
        aio_pika.Message(payload),
        routing_key=NOTIFY_QUEUE
    )

    await conn.close()
