from email.message import EmailMessage
import ssl
import smtplib
import os
import certifi
import sys

def send_email_service(email_request):

    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_receiver = email_request.email_receiver
    subject = email_request.subject
    body = email_request.body

    """
    Send an email to the user.
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context(cafile=certifi.where())
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    # Simulate sending an email
    print(f"Sending email to {email_request.email_receiver} with subject '{email_request.subject}' and body '{email_request.body}'")
    
    # Simulate a successful response
    response = {
        "status": "success",
        "message": f"Email to {email_request.email_receiver} with subject '{email_request.subject}' sent successfully"
    }
    
    return response


def preparePasswordSetEmailBody(req):
    """
    Prepare the body of the email to be sent to the user.
    """
    # Prepare the email body
    subject = "Establece tu contraseña"
    body = f"Hola, {req.name},\n\nBienvenid@ a tu Operador Civitech. \n\n Hemos recibido tu solicitud de transferencia y queremos contarte que la hemos acecptado. \n\nPara finalizar tu registro, por favor ingresa al siguiente enlace para establecer tu contraseña: {req.set_password_url}\n\n¡Bienvenido abordo!,\nTu equipo de Civitech"
    
    # Create a new request object with the email details

    email_request = {
        "email_receiver": req.email_receiver,
        "subject": subject,
        "body": body
    }
    
    # Send the email
    response = send_email_service(email_request)
    
    return response


def prepareInFileActionEmailBody(req):
    """
    Prepare the body of the email to be sent to the user.
    """
    # Prepare the email body
    subject = f"Acción realizada en tu archivo {req.file_name}"
    body = f"Hola, {req.name},\n\nLa acción de {req.action} fue realiza sobre tu archivo {req.file_name}. \n\n Para mayor verificación, ingresa tu carpeta y verifica dicha acción. \n\nSaludos,\nTu equipo de Civitech"
    
    # Create a new request object with the email details
    email_request = {
        "email_receiver": req.email_receiver,
        "subject": subject,
        "body": body
    }
    
    # Send the email
    response = send_email_service(email_request)
    
    return response