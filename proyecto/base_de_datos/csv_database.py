import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

SCHEMAS = {
    "usuarios": ["id", "username", "email", "nombre_completo", "activo", "fecha_registro"],
    "proyectos": ["id", "nombre", "descripcion", "fecha_creacion", "activo", "owner_username"],
    "tareas": ["id", "titulo", "descripcion", "estado", "prioridad", "fecha_creacion", "fecha_limite", "proyecto_id", "asignado_a"],
}

def init_db():
    DATA_DIR.mkdir(exist_ok=True)
    for tabla, columnas in SCHEMAS.items():
        archivo = DATA_DIR / f"{tabla}.csv"
        if not archivo.exists():
            with open(archivo, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=columnas)
                writer.writeheader()
            print(f"[DB] Tabla creada: {archivo.name}")

def get_csv_path(tabla: str) -> Path:
    return DATA_DIR / f"{tabla}.csv"

def get_columns(tabla: str) -> list[str]:
    return SCHEMAS[tabla]