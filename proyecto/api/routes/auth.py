from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from proyecto.auth.jwt_handler import crear_token
from proyecto.api.dependencies import get_usuario_repo
from proyecto.src.infrastructure.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    repo: UsuarioRepository = Depends(get_usuario_repo)
):
    resultado = repo.obtener_por_username(form.username)

    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    uid, usuario = resultado

    if not usuario.verificar_password(form.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "access_token": crear_token(usuario._username, uid),
        "token_type": "bearer"
    }