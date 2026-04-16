import os
from jose import jwt
import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Clave secreta (debe estar en .env y nunca en el código)
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"

# Generar un token JWT
def crear_token(user_id):
    if not user_id:
        raise ValueError("El ID de usuario es obligatorio")
    
    payload = {
        "sub": str(user_id),                # Subject (usuario)
        "iss": "miapp.com",                 # Emisor
        "aud": "miapp-usuarios",            # Audiencia
        "iat": datetime.datetime.utcnow(),  # Fecha de emisión
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)  # Expira en 15 min
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

# Verificar y decodificar un token JWT
def verificar_token(token):
    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            issuer="miapp.com",
            audience="miapp-usuarios"
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("El token ha expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")

