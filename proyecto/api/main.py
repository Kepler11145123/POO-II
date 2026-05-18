from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from proyecto.api.auth_router import router as auth_router
from proyecto.api.usuarios_router import router as usuarios_router
from proyecto.api.proyectos_router import router as proyectos_router
from proyecto.api.tareas_router import router as tareas_router
from proyecto.auth.jwt_handler import verificar_token
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="POO II — Sistema de Gestión de Proyectos",
    description=(
        "API REST para gestionar usuarios, proyectos y tareas.\n\n"
        "## Entidades\n"
        "- **Auth**: Login y generación de tokens JWT\n"
        "- **Usuarios**: crear y consultar usuarios del sistema\n"
        "- **Proyectos**: crear proyectos, asignar líderes y agregar tareas\n"
        "- **Tareas**: completar tareas y cambiar su prioridad\n\n"
        "## Status codes\n"
        "- `200` Operación exitosa\n"
        "- `201` Recurso creado\n"
        "- `404` Recurso no encontrado\n"
        "- `422` Error de validación"
    ),
    version="1.0.0",
)

templates = Jinja2Templates(directory="proyecto/templates")
app.mount("/static", StaticFiles(directory="proyecto/static"), name="static")

# Registra los routers — cada uno solo una vez
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(proyectos_router)
app.include_router(tareas_router)

@app.get("/status", tags=["Root"], summary="Estado de la API")
def root():
    return {"mensaje": "API funcionando", "docs": "/docs"}

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login", status_code=302)
    try:
        verificar_token(token)
    except ValueError:
        return RedirectResponse("/auth/login", status_code=302)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )
