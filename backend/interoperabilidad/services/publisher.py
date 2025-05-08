import json
from aio_pika import Message
from config.rabbitConfig import get_connection, USER_QUEUE, DOC_QUEUE, ID_USER_QUEUE

async def publishUserTransferMessages(req):
    user_payload = json.dumps({
        "id": req.id,
        "name": req.citizenName,
        "email": req.citizenEmail
    }).encode()
    doc_payload = json.dumps({
        "id": req.id, 
        "urlDocuments": req.urlDocuments,
        "confirmAPI": req.confirmAPI
    }).encode()

    print(f"Payload usuario: {user_payload}")

    conn = await get_connection()
    channel = await conn.channel()
    await channel.default_exchange.publish(Message(user_payload), routing_key=USER_QUEUE)
    await channel.default_exchange.publish(Message(doc_payload), routing_key=DOC_QUEUE)
    await conn.close()

async def publishUserIDConfirmationMessages(req):

    conn = await get_connection()
    channel = await conn.channel()
    await channel.default_exchange.publish(Message(req.id), routing_key=ID_USER_QUEUE)
    await conn.close()