from fastapi import APIRouter, Depends
from handlers.register_handler import RegisterCitizenHandler
from models.citizen_models import CitizenRegistrationRequest, CitizenRegistrationResponse

router = APIRouter(
    prefix="/register",
    tags=["register"]
)

@router.post("/", response_model=CitizenRegistrationResponse)
async def register_citizen(
    request: CitizenRegistrationRequest,
    handler: RegisterCitizenHandler = Depends()
):
    return await handler.handle(request)
