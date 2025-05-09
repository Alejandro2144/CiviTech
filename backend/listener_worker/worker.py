import json, asyncio
import httpx
from aio_pika import IncomingMessage
from rabbitConfig import get_connection, USER_QUEUE, DOC_QUEUE, ID_USER_QUEUE, UPLOAD_CONFIRM_QUEUE, NOTIFY_QUEUE
from dotenv import load_dotenv
from config.constants import CITIZEN_MS_URL, DOCUMENT_MS_URL, INTEROP_MS_URL
load_dotenv()

async def process_user(msg: IncomingMessage):
    data = json.loads(msg.body)

    # -> Aquí: comunicación HTTP al microservicio ciudadano
    async with httpx.AsyncClient() as client:
        await client.delete(f"{CITIZEN_MS_URL}/citizens/delete", json=data["id"])
    
    print(f"Usuario procesado: {data}", flush=True)

    await msg.ack()

async def process_docs(msg: IncomingMessage):
    payload = json.loads(msg.body)
    user_id = payload['id']
    urls = payload['urlDocuments']
    confirmAPI = payload['confirmAPI']

    '''docs_payload = {
        "id": user_id,
        "urlDocuments": urls,
        "confirmAPI": confirmAPI
    }'''


    # -> Aquí: comunicación HTTP al microservicio de documentos
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{DOCUMENT_MS_URL}/documents/recepcionInfoDocumentos",
            json={
                "id": user_id,
                "urlDocuments": urls,
                "confirmAPI": confirmAPI  # cambia si tienes una real
            }
        )
    
    print(f"Documentos procesados para el usuario {user_id}: {urls}", flush=True)
    
    await msg.ack()

async def process_id_user(msg: IncomingMessage):
    payload = json.loads(msg.body)
    id_payload = {
        "id": payload['id'],
    }

    # -> Aquí: comunicación HTTP al microservicio ciudadano para borrar el usuario
    async with httpx.AsyncClient() as client:
        try:
            await client.request(
                method="DELETE",
                url=f"{CITIZEN_MS_URL}/citizens/delete",
                data=json.dumps(id_payload),
                headers={"Content-Type": "application/json"}
            )
        except httpx.RequestError as e:
            print(f"Error contactando el microservicio de ciudadanos: {e}", flush=True)
            await msg.reject(requeue=False)
            return
        except httpx.HTTPStatusError as e:
            print(f"Error en la respuesta del microservicio de ciudadanos: {e}", flush=True)
            await msg.reject(requeue=False)
            return
        except Exception as e:
            print(f"Error inesperado: {e}", flush=True)
            await msg.reject(requeue=False)
            return
        

    # -> Aquí: comunicación HTTP al microservicio de documentos para borrar 
    #    los documentos de la carpeta con el id como nombre
    async with httpx.AsyncClient() as client:
        try:
            await client.request(
            method="DELETE",
            url=f"{DOCUMENT_MS_URL}/delete/folder/{id_payload['id']}",
            headers={"Content-Type": "application/json"}
            )
        except httpx.RequestError as e:
            print(f"Error contactando el microservicio de ciudadanos: {e}", flush=True)
            await msg.reject(requeue=False)
            return
        except httpx.HTTPStatusError as e:
            print(f"Error en la respuesta del microservicio de ciudadanos: {e}", flush=True)
            await msg.reject(requeue=False)
            return
        except Exception as e:
            print(f"Error inesperado: {e}", flush=True)
            await msg.reject(requeue=False)
            return
    
    print(f"ID Usuario Eliminado de BD y bucket: {id_payload['id']}", flush=True)
    
    await msg.ack()

async def process_confirmation(msg: IncomingMessage):
    confirmation_payload = json.loads(msg.body)

    # -> Aquí: comunicación HTTP al microservicio ciudadano para borrar el usuario
    async with httpx.AsyncClient() as client:
        await client.request(
        method="POST",
        url=INTEROP_MS_URL,
        data=json.dumps({
                            "id": confirmation_payload['id'], 
                            "req_status": confirmation_payload['req_status'],
                            "confirmAPI": confirmation_payload['confirmAPI']
                        }),
        headers={"Content-Type": "application/json"}
        )

    print(f"Usuario cargado a bucket: {confirmation_payload['id']}")
    
    await msg.ack()

    




async def process_notification(msg: IncomingMessage):
    notification_payload = json.loads(msg.body)

    # -> Aquí: comunicación HTTP al microservicio notificaciones para enviarle link al usuario
    '''async with httpx.AsyncClient() as client:
        await client.post(INTEROP_MS_URL, json=notification_payload)'''

    print(f"Enlace recibido: {notification_payload['set_password_url']}", flush=True)
    
    await msg.ack()



async def main():
    conn = await get_connection()
    chan = await conn.channel()
    user_q = await chan.declare_queue(USER_QUEUE, durable=True)
    doc_q  = await chan.declare_queue(DOC_QUEUE, durable=True)
    id_user_q = await chan.declare_queue(ID_USER_QUEUE, durable=True)
    upload_confirm_q = await chan.declare_queue(UPLOAD_CONFIRM_QUEUE, durable=True)
    notify_q = await chan.declare_queue(NOTIFY_QUEUE, durable=True)
    
    print("Worker listener iniciado...", flush=True)
    await user_q.consume(process_user)
    await doc_q.consume(process_docs)
    await id_user_q.consume(process_id_user)
    await upload_confirm_q.consume(process_confirmation)
    await notify_q.consume(process_notification)
    
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())