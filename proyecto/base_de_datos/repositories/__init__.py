"""
repositories/__init__.py — Almacén en memoria para usuarios, proyectos y tareas.

Expone el objeto `repositorio` usado por todos los routers.
"""
from proyecto.src.domain.usuario import Usuario
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.tarea import Tarea


class Repositorio:
    def __init__(self):
        self._usuarios: dict[int, Usuario]  = {}
        self._proyectos: dict[int, Proyecto] = {}
        self._tareas: dict[int, Tarea]      = {}
        self._next_usuario  = 1
        self._next_proyecto = 1
        self._next_tarea    = 1

    # ── Usuarios ──────────────────────────────────────────────────────────────

    def guardar_usuario(self, usuario: Usuario) -> int:
        uid = self._next_usuario
        self._usuarios[uid] = usuario
        self._next_usuario += 1
        return uid

    def obtener_usuario(self, uid: int) -> Usuario | None:
        return self._usuarios.get(uid)

    def listar_usuarios(self):
        return list(self._usuarios.items())

    # ── Proyectos ─────────────────────────────────────────────────────────────

    def guardar_proyecto(self, proyecto: Proyecto) -> int:
        pid = self._next_proyecto
        self._proyectos[pid] = proyecto
        self._next_proyecto += 1
        return pid

    def obtener_proyecto(self, pid: int) -> Proyecto | None:
        return self._proyectos.get(pid)

    def listar_proyectos(self):
        return list(self._proyectos.items())

    # ── Tareas ────────────────────────────────────────────────────────────────

    def guardar_tarea(self, tarea: Tarea) -> int:
        tid = self._next_tarea
        self._tareas[tid] = tarea
        self._next_tarea += 1
        return tid

    def obtener_tarea(self, tid: int) -> Tarea | None:
        return self._tareas.get(tid)

    def listar_tareas(self):
        return list(self._tareas.items())


# Instancia global compartida por todos los routers
repositorio = Repositorio()

# Alias para usuarios_router (usa nombre `usuario_repo`)
usuario_repo = repositorio