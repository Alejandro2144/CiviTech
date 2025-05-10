import json
import aio_pika
from utils.rabbit import get_connection

NOTIFY_QUEUE = "notify_citizen"  # Nombre de la cola donde interoperabilidad escucha confirmaciones

async def publish_notification_message(id_citizen: str, confirm_api: str, status: str = "1"):
    """
    Publica un mensaje de confirmación en la cola de transferencias confirmadas.
    """
    notification_payload = {
        "action": "in_file_action",
        "citizenEmail": citizenEmail,
        "req_status": status,
        "confirmAPI": confirm_api
    }

    print(f"[DEBUG] Publicando confirmación: {notification_payload}")

    connection = await get_connection()
    channel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(notification_payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=NOTIFY_QUEUE
    )

    await connection.close()