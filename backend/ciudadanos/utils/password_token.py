from jose import jwt
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def generate_set_password_token(user_id: int, email: str, expires_minutes: int = 1440):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "id": user_id,
        "email": email,
        "type": "set_password",
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_set_password_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "set_password":
            return None
        return payload
    except Exception:
        return None