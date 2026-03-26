"""
schemas.py — Modelos Pydantic para los cuerpos de request y response.

Pydantic valida automáticamente que los datos entrantes tengan el tipo
y formato correcto. Si no los tienen, FastAPI devuelve 422 automáticamente.

Separamos los schemas en:
  - Request: lo que el cliente ENVÍA  (campos requeridos para crear)
  - Response: lo que la API DEVUELVE  (incluye id y campos calculados)
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from src.domain.enums import PrioridadTarea, EstadoTarea


class UsuarioRequest(BaseModel):
    """Datos requeridos para crear un usuario."""
    username:        str
    email:           str
    nombre_completo: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username":        "juan123",
                "email":           "juan@mail.com",
                "nombre_completo": "Juan Pérez"
            }]
        }
    }

    @field_validator("username")
    @classmethod
    def validar_username(cls, valor):
        if len(valor) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        if not valor.isalnum():
            raise ValueError("Username solo puede contener letras y números")
        return valor

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor):
        partes = valor.split("@")
        if len(partes) != 2 or not partes[0] or "." not in partes[1] or not partes[1].split(".")[-1]:
            raise ValueError(f"Email inválido: {valor}")
        return valor


class UsuarioResponse(BaseModel):
    """Datos que devuelve la API al consultar un usuario."""
    id:              int
    username:        str
    email:           str
    nombre_completo: Optional[str]
    activo:          bool
    fecha_registro:  datetime

    model_config = {"from_attributes": True}


class ProyectoRequest(BaseModel):
    """Datos requeridos para crear un proyecto."""
    nombre:      str
    descripcion: Optional[str] = None
    lider_id:    Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "nombre":      "Sistema de Gestión",
                "descripcion": "Proyecto principal del semestre",
                "lider_id":    1
            }]
        }
    }

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        if len(valor.strip()) < 3:
            raise ValueError("El nombre del proyecto debe tener al menos 3 caracteres")
        return valor.strip()


class ProyectoResponse(BaseModel):
    """Datos que devuelve la API al consultar un proyecto."""
    id:            int
    nombre:        str
    descripcion:   Optional[str]
    lider_id:      Optional[int]
    total_tareas:  int
    fecha_creacion: datetime


class TareaRequest(BaseModel):
    """Datos requeridos para agregar una tarea a un proyecto."""
    titulo:      str
    descripcion: Optional[str]           = None
    prioridad:   Optional[PrioridadTarea] = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "titulo":      "Diseñar base de datos",
                "descripcion": "Modelo entidad-relación completo",
                "prioridad":   "Alta"
            }]
        }
    }

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor):
        if len(valor.strip()) < 3:
            raise ValueError("El título de la tarea debe tener al menos 3 caracteres")
        return valor.strip()


class TareaResponse(BaseModel):
    """Datos que devuelve la API al consultar una tarea."""
    id:               int
    titulo:           str
    descripcion:      Optional[str]
    estado:           EstadoTarea
    prioridad:        Optional[PrioridadTarea]
    fecha_creacion:   datetime
    fecha_completada: Optional[datetime]


class CambiarPrioridadRequest(BaseModel):
    """Body para cambiar la prioridad de una tarea."""
    prioridad: PrioridadTarea

    model_config = {
        "json_schema_extra": {
            "examples": [{"prioridad": "Alta"}]
        }
    }