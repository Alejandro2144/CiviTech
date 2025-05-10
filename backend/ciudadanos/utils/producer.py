import json
import aio_pika
from dotenv import load_dotenv
from config.constants import RABBIT_URL, NOTIFY_QUEUE
from utils.rabbit import get_connection
load_dotenv()

async def send_citizen_registered(name, email, url):

    payload = json.dumps({
        "action": "set_password",
        "citizenName": name,
        "citizenEmail": email,
        "passwordSetURL": url
    }).encode()

    print("🚀 Enviando a notify_citizen:", payload)

    connection = await get_connection()
    channel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=payload,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=NOTIFY_QUEUE
    )

    await connection.close()