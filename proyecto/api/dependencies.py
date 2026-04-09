from proyecto.base_de_datos.repositories.usuario_repo import UsuarioRepositoryJSON
from proyecto.base_de_datos.repositories.proyecto_repo import ProyectoRepositoryJSON
from proyecto.base_de_datos.repositories.tarea_repo import TareaRepositoryJSON

def get_usuario_repo() -> UsuarioRepositoryJSON:
    return UsuarioRepositoryJSON()

def get_proyecto_repo() -> ProyectoRepositoryJSON:
    return ProyectoRepositoryJSON()

def get_tarea_repo() -> TareaRepositoryJSON:
    return TareaRepositoryJSON()
