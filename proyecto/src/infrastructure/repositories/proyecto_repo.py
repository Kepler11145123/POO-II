from sqlalchemy.orm import Session
from database.models import Proyecto

class ProyectoRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, proyecto: Proyecto) -> Proyecto:
        self.db.add(proyecto)
        self.db.commit()
        self.db.refresh(proyecto)
        return proyecto

    def obtener(self, proyecto_id: str) -> Proyecto | None:
        return self.db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

    def listar(self, owner_id: str) -> list[Proyecto]:
        return self.db.query(Proyecto).filter(Proyecto.owner_id == owner_id).all()

    def eliminar(self, proyecto_id: str) -> bool:
        proyecto = self.obtener(proyecto_id)
        if not proyecto:
            return False
        self.db.delete(proyecto)
        self.db.commit()
        return True