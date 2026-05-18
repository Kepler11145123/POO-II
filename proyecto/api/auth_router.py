# proyecto/api/routes/auth.py
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from proyecto.auth.jwt_handler import crear_token
from proyecto.api.dependencies import get_usuario_repo
from proyecto.src.domain.usuario import Usuario
from database.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="proyecto/templates")

@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})


def registrar_usuario(
    repo: UsuarioRepository,
    username: str,
    email: str,
    nombre_completo: str | None,
    password: str,
    confirmar_password: str,
):
    username = username.strip()
    email = email.strip()
    nombre_completo = nombre_completo.strip() if nombre_completo else None

    if len(password) < 6:
        raise ValueError("La contrasena debe tener al menos 6 caracteres")
    if password != confirmar_password:
        raise ValueError("Las contrasenas no coinciden")
    if repo.obtener_por_username(username):
        raise ValueError("El usuario ya existe")
    if repo.obtener_por_email(email):
        raise ValueError("El email ya esta registrado")

    usuario = Usuario(
        username=username,
        email=email,
        nombre_completo=nombre_completo,
        password=password,
    )

    try:
        return repo.guardar(usuario)
    except IntegrityError as exc:
        repo.db.rollback()
        raise ValueError("El usuario o email ya esta registrado") from exc


@router.post("/register", response_class=HTMLResponse, include_in_schema=False)
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    nombre_completo: str = Form(""),
    password: str = Form(...),
    confirmar_password: str = Form(...),
    repo: UsuarioRepository = Depends(get_usuario_repo),
):
    form_values = {
        "username": username,
        "email": email,
        "nombre_completo": nombre_completo,
    }
    try:
        uid, usuario = registrar_usuario(
            repo=repo,
            username=username,
            email=email,
            nombre_completo=nombre_completo,
            password=password,
            confirmar_password=confirmar_password,
        )
    except ValueError as exc:
        return templates.TemplateResponse(
            request,
            "register.html",
            {"request": request, "error": str(exc), "form": form_values},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    token = crear_token(usuario.username, uid)
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax")
    return response


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
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax")
    return response

@router.post("/logout", response_class=HTMLResponse, include_in_schema=False)
def logout():
    response = RedirectResponse("/auth/login", status_code=302)
    response.delete_cookie("access_token")
    return response
