import json
from aio_pika import Message
from config.rabbitConfig import get_connection, USER_QUEUE, DOC_QUEUE

async def publish_transfer_messages(req):
    user_payload = json.dumps({
        "id": req.id,
        "name": req.citizenName,
        "email": req.citizenEmail
    }).encode()
    doc_payload = json.dumps({"id": req.id, "urlDocuments": req.urlDocuments}).encode()

    conn = await get_connection()
    channel = await conn.channel()
    await channel.default_exchange.publish(Message(user_payload), routing_key=USER_QUEUE)
    await channel.default_exchange.publish(Message(doc_payload), routing_key=DOC_QUEUE)
    await conn.close()