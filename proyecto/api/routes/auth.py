from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from proyecto.auth.jwt_handler import crear_token, verificar_token

router = APIRouter(prefix="/auth", tags=["auth"])

# Usuarios en memoria (o tu repositorio)
fake_users = {
    "yanier": {"id": "1", "username": "yanier", "hashed_password": "<hash aquí>"}
}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form.username)
    if not user or not verificar_token(form.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = crear_token({"sub": user["id"]})
    return {"access_token": token, "token_type": "bearer"}