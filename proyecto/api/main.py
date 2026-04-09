from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from proyecto.base_de_datos import init_db
from proyecto.base_de_datos.repositories import UsuarioRepositoryJSON as UsuarioRepository

from proyecto.api.routes.auth import router as auth_router
from proyecto.api.usuarios_router import router as usuarios_router
from proyecto.api.proyectos_router import router as proyectos_router
from proyecto.api.tareas_router import router as tareas_router


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

# templates y static para HTMX y Jinja2
templates= Jinja2Templates(directory="proyecto/templates")
app.mount("/static", StaticFiles(directory="proyecto/static"), name="static")

# Registra los routers — cada uno agrupa endpoints de una entidad
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(proyectos_router)
app.include_router(tareas_router)

# Inicializa los CSVs al arrancar (equivalente a create_all() en SQLAlchemy)
@app.on_event("startup")
def startup():
    init_db()

@app.get("/status", tags=["Root"], summary="Estado de la API")
def root():
    """Verifica que la API esté corriendo."""
    return {"mensaje": "API funcionando", "docs": "/docs"}

# Rutas HTML que devuelven templates jinja2
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse(
    request,
    "index.html",
    {"request": request}
)

# Ejemplo de uso en una ruta
@app.post("/usuarios/")
def crear_usuario(username: str, email: str):
    repo = UsuarioRepository()
    usuario = repo.crear(username=username, email=email)
    return usuario

