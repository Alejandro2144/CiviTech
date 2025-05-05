import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

load_dotenv()

TOKEN_SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_ALGORITHM = os.getenv("ALGORITHM", "HS256")

class JWTBearer(HTTPBearer):
    """
    Valida el token JWT en las rutas protegidas
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Formato de token inválido")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token inválido o expirado")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Token faltante")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
            return True
        except JWTError:
            return False

def decode_token(token: str):
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido o expirado")
