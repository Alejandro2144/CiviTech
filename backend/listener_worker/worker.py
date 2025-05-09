import os, json, asyncio
import httpx
from aio_pika import IncomingMessage
from rabbitConfig import get_connection, USER_QUEUE, DOC_QUEUE

# URLs de microservicios destino
CITIZEN_MS_URL  = os.getenv('CITIZEN_MS_URL', 'http://ciudadano:8001')
DOCUMENT_MS_URL = os.getenv('DOCUMENT_MS_URL', 'http://documentos:8002')

async def process_user(msg: IncomingMessage):
    data = json.loads(msg.body)

    # -> Aquí: comunicación HTTP al microservicio ciudadano
    '''async with httpx.AsyncClient() as client:
        await client.post(f"{CITIZEN_MS_URL}/api/users", json=data)'''
    
    print(f"Usuario procesado: {data}")

    await msg.ack()

async def process_docs(msg: IncomingMessage):
    payload = json.loads(msg.body)
    user_id = payload['id']
    urls = payload['urlDocuments']

    # -> Aquí: comunicación HTTP al microservicio de documentos
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DOCUMENT_MS_URL}/documents/recepcionInfoDocumentos",
            json={
            "id": user_id,
            "urlDocuments": urls,
            "confirmAPI": "http://example.com/api/transferCitizenConfirm"  # cambia si tienes una real
        }
        )
    
    print(f"Documentos procesados para el usuario {user_id}: {urls}")
    
    await msg.ack()

async def main():
    conn = await get_connection()
    chan = await conn.channel()
    user_q = await chan.declare_queue(USER_QUEUE, durable=True)
    doc_q  = await chan.declare_queue(DOC_QUEUE, durable=True)
    await user_q.consume(process_user)
    await doc_q.consume(process_docs)
    print("Worker listener iniciado...")
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())