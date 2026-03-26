import csv
import uuid
from datetime import datetime
from proyecto.base_de_datos.csv_database import get_csv_path, get_columns


class UsuarioRepository:

    def __init__(self):
        self.tabla = "usuarios"

    def _leer_todos(self) -> list[dict]:
        path = get_csv_path(self.tabla)
        with open(path, mode="r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _escribir_todos(self, registros: list[dict]):
        path = get_csv_path(self.tabla)
        columnas = get_columns(self.tabla)
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(registros)

    def crear(self, username: str, email: str, nombre_completo: str = None) -> dict:
        usuarios = self._leer_todos()
        for u in usuarios:
            if u["username"] == username:
                raise ValueError(f"El username '{username}' ya existe.")
            if u["email"] == email:
                raise ValueError(f"El email '{email}' ya está registrado.")

        nuevo = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "nombre_completo": nombre_completo or "",
            "activo": "True",
            "fecha_registro": datetime.now().isoformat(),
        }
        usuarios.append(nuevo)
        self._escribir_todos(usuarios)
        return nuevo

    def obtener_todos(self) -> list[dict]:
        return [u for u in self._leer_todos() if u["activo"] == "True"]

    def obtener_por_username(self, username: str) -> dict | None:
        for u in self._leer_todos():
            if u["username"] == username:
                return u
        return None