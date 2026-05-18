import os
from datetime import datetime, timedelta, timezone
from typing import Any

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

DEFAULT_JWT_SECRET = "dev-secret-key-change-me"
SECRET_KEY = os.getenv("JWT_SECRET", DEFAULT_JWT_SECRET)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


def crear_token(username: str, usuario_id: int, expires_delta: timedelta | None = None) -> str:
    if not username:
        raise ValueError("Username requerido para generar token")

    expires_at = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": username,
        "id": usuario_id,
        "exp": expires_at,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise ValueError("Token invalido o expirado") from exc

    if not payload.get("sub") or payload.get("id") is None:
        raise ValueError("Token sin datos de usuario")

    return payload


decode_token = verificar_token
