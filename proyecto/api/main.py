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