from sqlalchemy.orm import Session
from database.models import Tarea

class TareaRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, tarea: Tarea) -> Tarea:
        self.db.add(tarea)
        self.db.commit()
        self.db.refresh(tarea)
        return tarea

    def obtener(self, tarea_id: str) -> Tarea | None:
        return self.db.query(Tarea).filter(Tarea.id == tarea_id).first()

    def listar(self, proyecto_id: str) -> list[Tarea]:
        return self.db.query(Tarea).filter(Tarea.proyecto_id == proyecto_id).all()

    def eliminar(self, tarea_id: str) -> bool:
        tarea = self.obtener(tarea_id)
        if not tarea:
            return False
        self.db.delete(tarea)
        self.db.commit()
        return True