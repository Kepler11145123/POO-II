from sqlalchemy.orm import Session
from database.models import Usuario as UsuarioORM
from proyecto.src.domain.usuario import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, usuario: Usuario):
        orm = UsuarioORM(
            username        = usuario.username,
            email           = usuario.email,
            nombre_completo = usuario._nombre_completo,
            activo          = usuario._activo,
            password_hash   = usuario._password_hash
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return orm.id, usuario

    def obtener(self, usuario_id: int):
        orm = self.db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        return self._a_dominio(orm) if orm else None

    def obtener_por_username(self, username: str):
        orm = self.db.query(UsuarioORM).filter(UsuarioORM.username == username).first()
        if not orm:
            return None
        return orm.id, self._a_dominio(orm)

    def listar(self):
        return [(orm.id, self._a_dominio(orm)) for orm in self.db.query(UsuarioORM).all()]

    def eliminar(self, usuario_id: int) -> bool:
        orm = self.db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def _a_dominio(self, orm: UsuarioORM) -> Usuario:
        u = Usuario(username=orm.username, email=orm.email, nombre_completo=orm.nombre_completo)
        u._activo = orm.activo
        u._password_hash = orm.password_hash
        u.fecha_registro = orm.fecha_registro
        return u