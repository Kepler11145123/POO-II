from proyecto.src.infrastructure.repositories.usuario_repo import UsuarioRepository
from proyecto.src.infrastructure.repositories.proyecto_repo import ProyectoRepository
from proyecto.src.infrastructure.repositories.tarea_repo import TareaRepository

def get_usuario_repo() -> UsuarioRepository:
    return UsuarioRepository()

def get_proyecto_repo() -> ProyectoRepository:
    return ProyectoRepository()

def get_tarea_repo() -> TareaRepository:
    return TareaRepository()
