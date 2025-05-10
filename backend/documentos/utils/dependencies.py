from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from .token_client import validate_token_remote

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    payload = await validate_token_remote(token)
    return payload  # contiene id, email, exp

