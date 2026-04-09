import json
from ..csv_database import DATA_DIR
from proyecto.src.domain.proyecto import Proyecto
from .interfaces import IProyectoRepository

class ProyectoRepositoryJSON(IProyectoRepository):
    def __init__(self):
        self.archivo = DATA_DIR / "proyectos.json"

    def _leer_todo(self):
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar_todo(self, datos):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def guardar(self, proyecto: Proyecto):
        datos = self._leer_todo()
        nuevo_id = datos["next_id"]
        datos["proyectos"][str(nuevo_id)] = proyecto.to_dict()
        datos["next_id"] += 1
        self._guardar_todo(datos)
        return nuevo_id, proyecto

    def obtener(self, proyecto_id: int):
        datos = self._leer_todo()
        p_data = datos["proyectos"].get(str(proyecto_id))
        return Proyecto.from_dict(p_data) if p_data else None

    def listar(self):
        datos = self._leer_todo()
        return [(int(pid), Proyecto.from_dict(p)) for pid, p in datos["proyectos"].items()]

    def eliminar(self, proyecto_id: int):
        datos = self._leer_todo()
        if str(proyecto_id) in datos["proyectos"]:
            del datos["proyectos"][str(proyecto_id)]
            self._guardar_todo(datos)
            return True
        return False