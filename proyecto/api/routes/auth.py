from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# Ajustamos las rutas para que apunten a la estructura de tu proyecto
from proyecto.auth.jwt_handler import crear_token
from proyecto.api.dependencies import get_usuario_repo

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    repo = Depends(get_usuario_repo)
):
    # Buscamos al usuario por su username
    resultado = repo.obtener_por_username(form.username)
    
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    uid, usuario = resultado
    
    # Verificamos la contraseña usando el método que definimos en la clase Usuario
    if not usuario.verificar_password(form.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Si todo está bien, generamos el token
    return {
        "access_token": crear_token(usuario._username, uid), # Usamos _username por tu clase Usuario
        "token_type": "bearer"
    }