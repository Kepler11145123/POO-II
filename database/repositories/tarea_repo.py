from sqlalchemy.orm import Session
from database.models import Tarea as TareaORM
from proyecto.src.domain.tarea import Tarea

class TareaRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, tarea: Tarea, proyecto_id: int):
        orm = TareaORM(
            titulo       = tarea._titulo,
            descripcion  = tarea.descripcion,
            estado       = tarea._estado,
            prioridad    = tarea._prioridad,
            proyecto_id  = proyecto_id,
            asignado_a   = None
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return orm.id, tarea

    def obtener(self, tarea_id: int):
        orm = self.db.query(TareaORM).filter(TareaORM.id == tarea_id).first()
        return self._a_dominio(orm) if orm else None

    def listar(self):
        return [(orm.id, self._a_dominio(orm)) for orm in self.db.query(TareaORM).all()]

    def actualizar(self, tarea_id: int, tarea: Tarea):
        orm = self.db.query(TareaORM).filter(TareaORM.id == tarea_id).first()
        if not orm:
            return None
        orm.estado           = tarea._estado
        orm.prioridad        = tarea._prioridad
        orm.fecha_completada = tarea._fecha_completada
        self.db.commit()
        self.db.refresh(orm)
        return tarea_id, tarea

    def eliminar(self, tarea_id: int) -> bool:
        orm = self.db.query(TareaORM).filter(TareaORM.id == tarea_id).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def _a_dominio(self, orm: TareaORM) -> Tarea:
        t = Tarea(titulo=orm.titulo, descripcion=orm.descripcion)
        t._estado           = orm.estado
        t._prioridad        = orm.prioridad
        t.fecha_creacion    = orm.fecha_creacion
        t._fecha_completada = orm.fecha_completada
        return t