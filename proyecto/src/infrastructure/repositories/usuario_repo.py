from sqlalchemy.orm import Session
from database.models import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener(self, usuario_id: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_por_username(self, username: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def listar(self) -> list[Usuario]:
        return self.db.query(Usuario).all()

    def eliminar(self, usuario_id: str) -> bool:
        usuario = self.obtener(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True