# proyecto/api/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from proyecto.auth.jwt_handler import crear_token
from proyecto.api.dependencies import get_usuario_repo
from database.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="proyecto/templates")

@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    repo: UsuarioRepository = Depends(get_usuario_repo)
):
    resultado = repo.obtener_por_username(form.username)
    if not resultado:
        return templates.TemplateResponse(request, "login.html", {"request": request, "error": "Credenciales incorrectas"}, status_code=401)
    uid, usuario = resultado
    if not usuario.verificar_password(form.password):
        return templates.TemplateResponse(request, "login.html", {"request": request, "error": "Credenciales incorrectas"}, status_code=401)
    
    token = crear_token(usuario._username, uid)
    
    # Set cookie and redirect to dashboard
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@router.post("/logout", response_class=HTMLResponse, include_in_schema=False)
def logout():
    response = RedirectResponse("/auth/login", status_code=302)
    response.delete_cookie("access_token")
    return response