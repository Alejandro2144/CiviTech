from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Token inválido o expirado.")

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token inválido o expirado.")
            
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="No autorizado.")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = decode_token(jwtoken)
        return payload is not None
