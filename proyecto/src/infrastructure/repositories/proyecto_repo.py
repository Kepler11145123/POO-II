from sqlalchemy.orm import Session
from database.models import Proyecto as ProyectoORM
from proyecto.src.domain.proyecto import Proyecto

class ProyectoRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, proyecto: Proyecto):
        # Convierte dominio → ORM
        orm = ProyectoORM(
            nombre      = proyecto.nombre,
            descripcion = proyecto.descripcion,
            lider_id    = proyecto.lider.id if proyecto.lider else None
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return orm.id, proyecto

    def obtener(self, proyecto_id: int):
        orm = self.db.query(ProyectoORM).filter(ProyectoORM.id == proyecto_id).first()
        if not orm:
            return None
        return self._a_dominio(orm)

    def listar(self):
        return [(orm.id, self._a_dominio(orm)) for orm in self.db.query(ProyectoORM).all()]

    def eliminar(self, proyecto_id: int) -> bool:
        orm = self.db.query(ProyectoORM).filter(ProyectoORM.id == proyecto_id).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def _a_dominio(self, orm: ProyectoORM) -> Proyecto:
        # Convierte ORM → dominio
        p = Proyecto(nombre=orm.nombre, descripcion=orm.descripcion)
        p.fecha_creacion = orm.fecha_creacion
        return p