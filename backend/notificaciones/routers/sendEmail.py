from fastapi import APIRouter, HTTPException, status
from schemas import *
from services import *

notificationsRouter = APIRouter()

@notificationsRouter.post("/sendPasswordSetEmail")
async def sendPasswordSetEmail(req: PasswordEmailPayload):
    """
    Send an email to the user when being transfered to us to set the password.
    """
    # Call the email service to send the email
    try:
        response = await preparePasswordSetEmailBody(req)
        return {"status": "Email sent successfully", "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}"
        )
    
@notificationsRouter.post("/sendInFileActionEmail")
async def sendInFileActionEmail(req: InFileActionEmailPayload):
    """
    Send an email to the user when an action is made to a file (delete, update, upload).
    """
    # Call the email service to send the email
    try:
        response = await prepareInFileActionEmailBody(req)
        return {"status": "Email sent successfully", "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}"
        )