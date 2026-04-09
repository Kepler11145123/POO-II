from pathlib import Path
import json

DATA_DIR = Path(__file__).parent.parent / "data"

def init_db():
    """Crea los archivos json si es que no existen al arrancar el servidor"""
    DATA_DIR.mkdir(exist_ok=True)
    for nombre, estructura in [
        ("usuarios.json", {"usuarios": {}, "next_id": 1}),
        ("proyectos.json", {"proyectos": {}, "next_id": 1}),
        ("tareas.json", {"tareas": {}, "next_id": 1}),
    
    ]:
        archivo = DATA_DIR / nombre
        if not archivo.exists():
            archivo.write_text(json.dumps(estructura, indent=2, ensure_ascii=False))