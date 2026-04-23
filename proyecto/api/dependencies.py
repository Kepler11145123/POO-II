from fastapi import Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from proyecto.src.infrastructure.repositories.usuario_repo import UsuarioRepository
from proyecto.src.infrastructure.repositories.proyecto_repo import ProyectoRepository
from proyecto.src.infrastructure.repositories.tarea_repo import TareaRepository

def get_usuario_repo(db: Session = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepository(db)

def get_proyecto_repo(db: Session = Depends(get_db)) -> ProyectoRepository:
    return ProyectoRepository(db)

def get_tarea_repo(db: Session = Depends(get_db)) -> TareaRepository:
    return TareaRepository(db)