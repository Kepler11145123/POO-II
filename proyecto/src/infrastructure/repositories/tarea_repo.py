import json
from ..csv_database import DATA_DIR
from proyecto.src.domain.tarea import Tarea
from .interfaces import ITareaRepository

class TareaRepositoryJSON(ITareaRepository):
    def __init__(self):
        self.archivo = DATA_DIR / "tareas.json"

    def _leer_todo(self):
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar_todo(self, datos):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def guardar(self, tarea: Tarea):
        datos = self._leer_todo()
        nuevo_id = datos["next_id"]
        datos["tareas"][str(nuevo_id)] = tarea.to_dict()
        datos["next_id"] += 1
        self._guardar_todo(datos)
        return nuevo_id, tarea

    def obtener(self, tarea_id: int):
        datos = self._leer_todo()
        t_data = datos["tareas"].get(str(tarea_id))
        return Tarea.from_dict(t_data) if t_data else None

    def listar(self):
        datos = self._leer_todo()
        return [(int(tid), Tarea.from_dict(t)) for tid, t in datos["tareas"].items()]

    def eliminar(self, tarea_id: int):
        datos = self._leer_todo()
        if str(tarea_id) in datos["tareas"]:
            del datos["tareas"][str(tarea_id)]
            self._guardar_todo(datos)
            return True
        return False