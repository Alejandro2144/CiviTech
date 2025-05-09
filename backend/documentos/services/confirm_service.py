import json
import aio_pika
from utils.rabbit import get_connection

CONFIRMATION_QUEUE = "transferencias_confirmadas"  # Nombre de la cola donde interoperabilidad escucha confirmaciones

async def publish_confirmation_message(id_citizen: str, confirm_api: str, status: str = "1"):
    """
    Publica un mensaje de confirmación en la cola de transferencias confirmadas.
    """
    confirmation_payload = {
        "id": id_citizen,
        "req_status": status,
        "confirmAPI": confirm_api
    }

    print(f"[DEBUG] Publicando confirmación: {confirmation_payload}")

    connection = await get_connection()
    channel = await connection.channel()

    await channel.declare_queue(CONFIRMATION_QUEUE, durable=True)

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(confirmation_payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=CONFIRMATION_QUEUE
    )

    await connection.close()
