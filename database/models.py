from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    proyectos = relationship("Proyecto", back_populates="owner")

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("usuarios.id"), nullable=False)

    owner = relationship("Usuario", back_populates="proyectos")
    tareas = relationship("Tarea", back_populates="proyecto")

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String, nullable=False)
    completada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    proyecto_id = Column(String, ForeignKey("proyectos.id"), nullable=False)

    proyecto = relationship("Proyecto", back_populates="tareas")