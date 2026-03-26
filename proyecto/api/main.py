"""
main.py — Punto de entrada de la aplicación FastAPI.

Ejecutar con:
    uvicorn proyecto.api.main:app --reload

Documentación automática disponible en:
    http://localhost:8000/docs      (Swagger UI)
    http://localhost:8000/redoc     (ReDoc)
"""
from fastapi import FastAPI
from proyecto.api.usuarios_router import router as usuarios_router
from proyecto.api.proyectos_router import router as proyectos_router
from proyecto.api.tareas_router import router as tareas_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.routes import proyectos_router, tareas_router

app = FastAPI(
    title="POO II — Sistema de Gestión de Proyectos",
    description=(
        "API REST para gestionar usuarios, proyectos y tareas.\n\n"
        "## Entidades\n"
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
templates= Jinja2Templates(directory="proyecto/api/templates")
app.mount("/static", StaticFiles(directory="proyecto/api/static"), name="static")

# Registra los routers — cada uno agrupa endpoints de una entidad
app.include_router(usuarios_router)
app.include_router(proyectos_router)
app.include_router(tareas_router)


@app.get("/", tags=["Root"], summary="Estado de la API")
def root():
    """Verifica que la API esté corriendo."""
    return {"mensaje": "API funcionando", "docs": "/docs"}


from fastapi import FastAPI
from base_de_datos.csv_database import init_db

app = FastAPI()

# Inicializa los CSVs al arrancar (equivalente a create_all() en SQLAlchemy)
@app.on_event("startup")
def startup():
    init_db()

# Ejemplo de uso en una ruta
from base_de_datos.repositories.usuario_repo import UsuarioRepository

@app.post("/usuarios/")
def crear_usuario(username: str, email: str):
    repo = UsuarioRepository()
    usuario = repo.crear(username=username, email=email)
    return usuario

