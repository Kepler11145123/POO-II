from datetime import datetime
from typing import Optional
from .enums import PrioridadTarea, EstadoTarea


class Tarea:
    def __init__(self, titulo: str, descripcion: Optional[str] = None, prioridad: PrioridadTarea = None) -> None:
        if len(titulo) < 3:
            raise ValueError("El título de la tarea debe tener al menos 3 caracteres.")

        self._titulo = titulo
        self.descripcion = descripcion
        self._prioridad = prioridad
        self._estado = EstadoTarea.PENDIENTE
        self.fecha_creacion = datetime.now()
        self._fecha_completada: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "titulo": self._titulo,
            "descripcion": self.descripcion,
            "prioridad": self._prioridad.value if self._prioridad else None,
            "estado": self._estado.value,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_completada": self._fecha_completada.isoformat() if self._fecha_completada else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tarea":
        t = cls(
            titulo=data["titulo"],
            descripcion=data.get("descripcion"),
            prioridad=PrioridadTarea(data["prioridad"]) if data.get("prioridad") else None
        )
        t._estado = EstadoTarea(data["Estado"])
        t.fecha_creacion = datetime.fromisoformat(data["fecha_creacion"])
        if data.get("fecha_completada"):
            t._fecha_completada = datetime.fromisoformat(data["fecha_completada"])
            return t

    def completar(self) -> None:
        self._estado = EstadoTarea.COMPLETADA
        self._fecha_completada = datetime.now()

    def cambiar_prioridad(self, nueva_prioridad: PrioridadTarea) -> None:
        self._prioridad = nueva_prioridad

    def iniciar(self) -> None:
        self._estado = EstadoTarea.EN_PROGRESO

    def __str__(self) -> str:
        return f"{self._titulo} [{self._prioridad}] - {self._estado}"
