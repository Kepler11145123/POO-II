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

    def completar(self) -> None:
        self._estado = EstadoTarea.COMPLETADA
        self._fecha_completada = datetime.now()

    def cambiar_prioridad(self, nueva_prioridad: PrioridadTarea) -> None:
        self._prioridad = nueva_prioridad

    def iniciar(self) -> None:
        self._estado = EstadoTarea.EN_PROGRESO

    def __str__(self) -> str:
        return f"{self._titulo} [{self._prioridad}] - {self._estado}"
