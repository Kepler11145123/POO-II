from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id              = Column(Integer, primary_key=True)
    username        = Column(String(50),  nullable=False, unique=True)
    email           = Column(String(255), nullable=False, unique=True)
    nombre_completo = Column(String(100))
    activo          = Column(Boolean, default=True)
    password_hash   = Column(String(255))
    rol             = Column(String(20), default="usuario")
    fecha_registro  = Column(DateTime, default=datetime.utcnow)

    proyectos_liderados = relationship("Proyecto", back_populates="lider")
    tareas_asignadas    = relationship("Tarea", back_populates="asignado")

class Proyecto(Base):
    __tablename__ = "proyectos"

    id             = Column(Integer, primary_key=True)
    nombre         = Column(String(100), nullable=False)
    descripcion    = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    activo         = Column(Boolean, default=True)
    lider_id       = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))

    lider  = relationship("Usuario", back_populates="proyectos_liderados")
    tareas = relationship("Tarea", back_populates="proyecto", cascade="all, delete")

class Tarea(Base):
    __tablename__ = "tareas"

    id               = Column(Integer, primary_key=True)
    titulo           = Column(String(200), nullable=False)
    descripcion      = Column(Text)
    estado           = Column(String(20),  default="Pendiente")
    prioridad        = Column(String(10))
    fecha_creacion   = Column(DateTime, default=datetime.utcnow)
    fecha_completada = Column(DateTime)
    fecha_limite     = Column(DateTime)
    proyecto_id      = Column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    asignado_a       = Column(Integer, ForeignKey("usuarios.id",  ondelete="SET NULL"))

    proyecto = relationship("Proyecto", back_populates="tareas")
    asignado = relationship("Usuario",  back_populates="tareas_asignadas")