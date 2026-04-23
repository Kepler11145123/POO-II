import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "CAMBIAR-ESTO")
ALGORITHM = "HS256"

def crear_token(username: str, usuario_id: int) -> str:
    payload = {
        "sub": username,
        "id": usuario_id,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ValueError("Token inválido o expirado")