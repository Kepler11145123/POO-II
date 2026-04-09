import json
from pathlib import Path
from ..csv_database import DATA_DIR
from proyecto.src.domain.usuario import Usuario
from .interfaces import IUsuarioRepository

class UsuarioRepositoryJSON(IUsuarioRepository):
    def __init__(self):
        self.archivo = DATA_DIR / "usuarios.json"

    def _leer_todo(self):
        with open(self.archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar_todo(self, datos):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def guardar(self, usuario: Usuario):
        datos = self._leer_todo()
        nuevo_id = datos["next_id"]
        
        # Usamos el to_dict que creamos antes
        datos["usuarios"][str(nuevo_id)] = usuario.to_dict()
        datos["next_id"] += 1
        
        self._guardar_todo(datos)
        return nuevo_id, usuario

    def obtener_por_username(self, username: str):
        datos = self._leer_todo()
        for uid, u_data in datos["usuarios"].items():
            if u_data["username"] == username:
                return int(uid), Usuario.from_dict(u_data)
        return None

    def obtener(self, usuario_id: int):
        datos = self._leer_todo()
        u_data = datos["usuarios"].get(str(usuario_id))
        return Usuario.from_dict(u_data) if u_data else None

    def listar(self):
        datos = self._leer_todo()
        return [(int(uid), Usuario.from_dict(u)) for uid, u in datos["usuarios"].items()]

    def eliminar(self, usuario_id: int):
        datos = self._leer_todo()
        if str(usuario_id) in datos["usuarios"]:
            del datos["usuarios"][str(usuario_id)]
            self._guardar_todo(datos)
            return True
        return False