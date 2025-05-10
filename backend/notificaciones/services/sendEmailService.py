from email.message import EmailMessage
import ssl
import smtplib
import os
import certifi
import sys

async def send_email_service(email_request):

    email_sender = os.getenv("SENDER_EMAIL")
    email_password = os.getenv("SENDER_PASSWORD")
    email_receiver = email_request["email_receiver"]
    subject = email_request["subject"]
    body = email_request["body"]

    """
    Send an email to the user.
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    print(email_receiver, flush=True)
    print(email_sender, flush=True)
    print(subject, flush=True)
    print(body, flush=True)

    context = ssl.create_default_context(cafile=certifi.where())
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    # Simulate sending an email
    print(f"Sending email to {email_receiver}")
    
    # Simulate a successful response
    return {
        "status": "success",
        "message": f"Email to {email_receiver} with subject '{subject}' sent successfully."
    }


async def preparePasswordSetEmailBody(req):
    """
    Prepare the body of the email to be sent to the user.
    """
    # Prepare the email body
    subject = "Establece tu contraseña"
    body = f"Hola, {req.citizenName},\n\nBienvenid@ a tu Operador Civitech. \n\n Hemos recibido tu solicitud de transferencia y queremos contarte que la hemos acecptado. \n\nPara finalizar tu registro, por favor ingresa al siguiente enlace para establecer tu contraseña: {req.passwordSetURL}\n\n¡Bienvenido abordo!,\nTu equipo de Civitech"
    
    # Create a new request object with the email details

    email_request = {
        "email_receiver": req.citizenEmail,
        "subject": subject,
        "body": body
    }
    
    # Send the email
    response = await send_email_service(email_request)
    
    return response


async def prepareInFileActionEmailBody(req):
    """
    Prepare the body of the email to be sent to the user.
    """
    # Prepare the email body
    subject = f"Acción realizada en tu archivo {req.fileName}"
    body = f"Hola, {req.citizenName},\n\nLa acción de {req.fileAction} fue realizada sobre su archivo {req.fileName}. \n\n Para verificar, ingrese a su carpeta y verifique dicha acción. \n\nSaludos,\nTu equipo de Civitech"
    
    # Create a new request object with the email details
    email_request = {
        "email_receiver": req.citizenEmail,
        "subject": subject,
        "body": body
    }
    
    # Send the email
    response = await send_email_service(email_request)
    
    return response
