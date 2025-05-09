import os, json, asyncio
import httpx
from aio_pika import IncomingMessage
from rabbitConfig import get_connection, USER_QUEUE, DOC_QUEUE, ID_USER_QUEUE, UPLOAD_CONFIRM_QUEUE

# URLs de microservicios destino
CITIZEN_MS_URL  = os.getenv('CITIZEN_MS_URL', 'http://ciudadano:8001')
DOCUMENT_MS_URL = os.getenv('DOCUMENT_MS_URL', 'http://documentos:8002')
INTEROP_MS_URL = os.getenv('INTEROP_MS_URL', 'http://0.0.0.0:8000/confirmTransfer')

async def process_user(msg: IncomingMessage):
    data = json.loads(msg.body)

    # -> Aquí: comunicación HTTP al microservicio ciudadano
    '''async with httpx.AsyncClient() as client:
        await client.post(f"{CITIZEN_MS_URL}/api/users", json=data)'''
    
    print(f"Usuario procesado: {data}", flush=True)

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
    
    print(f"Documentos procesados para el usuario {user_id}: {urls}", flush=True)
    
    await msg.ack()

async def process_id_user(msg: IncomingMessage):
    payload = json.loads(msg.body)
    user_id = payload['id']

    # -> Aquí: comunicación HTTP al microservicio ciudadano para borrar el usuario
    '''async with httpx.AsyncClient() as client:
        await client.post(f"{CITIZEN_MS_URL}/api/users", json=data)'''

    # -> Aquí: comunicación HTTP al microservicio de documentos para borrar 
    #    los documentos de la carpeta con el id como nombre
    '''async with httpx.AsyncClient() as client:
        await client.post(
            f"{DOCUMENT_MS_URL}/api/documents/process",
            json={"id": user_id, "urls": urls}
        )'''
    
    print(f"ID Usuario Eliminado de BD y bucket: {user_id}")
    
    await msg.ack()

async def process_confirmation(msg: IncomingMessage):
    confirmation_payload = json.loads(msg.body)

    # -> Aquí: comunicación HTTP al microservicio ciudadano para borrar el usuario
    async with httpx.AsyncClient() as client:
        await client.post(INTEROP_MS_URL, json=confirmation_payload)

    print(f"ID Usuario Cargado a BD y bucket: {confirmation_payload['id']}")
    
    await msg.ack()

async def main():
    conn = await get_connection()
    chan = await conn.channel()
    user_q = await chan.declare_queue(USER_QUEUE, durable=True)
    doc_q  = await chan.declare_queue(DOC_QUEUE, durable=True)
    id_user_q = await chan.declare_queue(ID_USER_QUEUE, durable=True)
    upload_confirm_q = await chan.declare_queue(UPLOAD_CONFIRM_QUEUE, durable=True)
    print("Worker listener iniciado...", flush=True)
    await user_q.consume(process_user)
    await doc_q.consume(process_docs)
    await id_user_q.consume(process_id_user)
    await upload_confirm_q.consume(process_confirmation)
    
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())