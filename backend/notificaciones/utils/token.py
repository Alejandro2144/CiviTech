
''
''' Use whatever may be needed from this code.'''
''

# from datetime import datetime, timedelta, timezone
# from jose import JWTError, jwt
# from fastapi import Request, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# SECRET_KEY = "passwordsecret123"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def createAccessToken(data: dict, expires_delta: timedelta = None):
#     toEncode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     toEncode.update({"exp": expire})
#     encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
#     return encodedJwt

# def decodeToken(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         return None

# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Token inválido o expirado.")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Token inválido o expirado.")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="No se proporcionó un token de acceso")

#     def verify_jwt(self, jwtoken):
#         isTokenValid = False
#         try:
#             payload = decodeToken(jwtoken)
#         except:
#             payload = None
#         if payload:
#             isTokenValid = True
#         return isTokenValid