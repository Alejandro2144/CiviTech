from fastapi import APIRouter, HTTPException, Depends, Request
from ..schemas.token import TokenRequest, TokenResponse, TokenPayload
from ..utils.token import create_access_token, decode_token, JWTBearer

router = APIRouter(prefix="/token", tags=["Token"])

@router.post("/generate", response_model=TokenResponse)
async def generate_token(data: TokenRequest):
    token = create_access_token(data=data.dict())
    return TokenResponse(access_token=token)

@router.post("/validate", response_model=TokenPayload)
async def validate_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=403, detail="Token requerido.")

    token = auth_header.split(" ")[1]
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=403, detail="Token inválido o expirado.")

    return payload
