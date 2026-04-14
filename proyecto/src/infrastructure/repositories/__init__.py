from .usuario_repo import UsuarioRepositoryJSON
from .proyecto_repo import ProyectoRepositoryJSON
from .tarea_repo import TareaRepositoryJSON

_usuario_repo = UsuarioRepositoryJSON()
_proyecto_repo = ProyectoRepositoryJSON()
_tarea_repo = TareaRepositoryJSON()

class _Repositorio:
    def guardar_usuario(self, usuario):
        return _usuario_repo.guardar(usuario)
    def obtener_usuario(self, uid):
        return _usuario_repo.obtener(uid)
    def listar_usuarios(self):
        return _usuario_repo.listar()
    def guardar_proyecto(self, proyecto):
        return _proyecto_repo.guardar(proyecto)
    def obtener_proyecto(self, pid):
        return _proyecto_repo.obtener(pid)
    def listar_proyectos(self):
        return _proyecto_repo.listar()
    def guardar_tarea(self, tarea):
        return _tarea_repo.guardar(tarea)
    def obtener_tarea(self, tid):
        return _tarea_repo.obtener(tid)
    def listar_tareas(self):
        return _tarea_repo.listar()

repositorio = _Repositorio()

obtener_tarea = repositorio.obtener_tarea
guardar_tarea = repositorio.guardar_tarea