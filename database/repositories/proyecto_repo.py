from sqlalchemy.orm import Session
from database.models import Proyecto as ProyectoORM, Usuario as UsuarioORM
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.usuario import Usuario

class ProyectoRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, proyecto: Proyecto, lider_id: int | None = None):
        lider_id = lider_id if lider_id is not None else getattr(proyecto.lider, "id", None)
        orm = ProyectoORM(
            nombre      = proyecto.nombre,
            descripcion = proyecto.descripcion,
            lider_id    = lider_id
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        proyecto.id = orm.id
        return orm.id, proyecto

    def obtener(self, proyecto_id: int):
        orm = self.db.query(ProyectoORM).filter(ProyectoORM.id == proyecto_id).first()
        return self._a_dominio(orm) if orm else None

    def obtener_para_lider(self, proyecto_id: int, lider_id: int):
        orm = (
            self.db.query(ProyectoORM)
            .filter(ProyectoORM.id == proyecto_id, ProyectoORM.lider_id == lider_id)
            .first()
        )
        return self._a_dominio(orm) if orm else None

    def listar(self):
        return [(orm.id, self._a_dominio(orm)) for orm in self.db.query(ProyectoORM).all()]

    def listar_por_lider(self, lider_id: int):
        return [
            (orm.id, self._a_dominio(orm))
            for orm in self.db.query(ProyectoORM).filter(ProyectoORM.lider_id == lider_id).all()
        ]

    def actualizar(self, proyecto_id: int, proyecto: Proyecto):
        orm = self.db.query(ProyectoORM).filter(ProyectoORM.id == proyecto_id).first()
        if not orm:
            return None
        orm.nombre      = proyecto.nombre
        orm.descripcion = proyecto.descripcion
        orm.lider_id    = proyecto.lider.id if proyecto.lider else None
        self.db.commit()
        self.db.refresh(orm)
        return orm.id, proyecto
    
    def eliminar(self, proyecto_id: int) -> bool:
        orm = self.db.query(ProyectoORM).filter(ProyectoORM.id == proyecto_id).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def eliminar_para_lider(self, proyecto_id: int, lider_id: int) -> bool:
        orm = (
            self.db.query(ProyectoORM)
            .filter(ProyectoORM.id == proyecto_id, ProyectoORM.lider_id == lider_id)
            .first()
        )
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def _a_dominio(self, orm: ProyectoORM) -> Proyecto:
        # Construye el lider si existe
        lider = None
        if orm.lider:
            lider = Usuario(
                username=orm.lider.username,
                email=orm.lider.email,
                nombre_completo=orm.lider.nombre_completo
            )
            lider.id = orm.lider.id
            lider._activo = orm.lider.activo

        p = Proyecto(nombre=orm.nombre, descripcion=orm.descripcion, lider=lider)
        p.id = orm.id
        p.fecha_creacion = orm.fecha_creacion

        # Carga las tareas relacionadas
        from proyecto.src.domain.tarea import Tarea
        from proyecto.src.domain.enums import PrioridadTarea, EstadoTarea
        for t_orm in orm.tareas:
            t = Tarea(titulo=t_orm.titulo, descripcion=t_orm.descripcion)
            t._estado = t_orm.estado
            t._prioridad = t_orm.prioridad
            t.fecha_creacion = t_orm.fecha_creacion
            t._id = t_orm.id
            p.tareas.append(t)

        return p
