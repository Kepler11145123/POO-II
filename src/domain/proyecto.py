from datetime import datetime
from typing import Optional
from .usuario import Usuario
from .tarea import Tarea
from .enums import PrioridadTarea, EstadoTarea

class Proyecto:
    def __init__(self, nombre:str, descripcion:Optional[str] = None, lider:Usuario = None) -> None:

        if len (nombre) < 3:
            raise ValueError("El nombre del proyecto debe tener al menos 3 caracteres.")
        
        if lider and not isinstance(lider, Usuario):
            raise ValueError("El líder del proyecto debe ser un usuario válido.")
        
        self._nombre = nombre
        self._descripcion = descripcion
        self.fecha_creacion = datetime.now()
        self._tareas: list[Tarea] = []
        self._lider = None
        self.lider = lider

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def descripcion(self) -> Optional[str]:
        return self._descripcion
    
    @property
    def lider(self) -> Usuario:
        return self._lider
    
    @lider.setter
    def lider(self, valor) -> None:
        self._lider = valor
    
    @property
    def tareas(self) -> list:
        return self._tareas
    
    def agregar_tarea(self, tarea:Tarea) -> None:
        if not isinstance(tarea, Tarea):
            raise ValueError("Solo se pueden agregar objetos de tipo Tarea.")
        self._tareas.append(tarea)

    def obtener_tareas_pendientes(self) -> list[Tarea]:
        return [tarea for tarea in self._tareas if tarea._estado == EstadoTarea.PENDIENTE]
    
    def obtener_tareas_por_prioridad(self, prioridad:PrioridadTarea) -> list[Tarea]:
        return [tarea for tarea in self._tareas if tarea._prioridad == prioridad]
        
    def __str__(self):
        return f"Proyecto: {self.nombre}, Líder: {self.lider._nombre_completo if self.lider else 'Sin líder'}"