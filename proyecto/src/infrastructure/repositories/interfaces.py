from abc import ABC, abstractmethod
from typing import Optional, List

class IUsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario) -> tuple:
        pass
    @abstractmethod
    def obtener(self, usuario_id: int):
        pass
    @abstractmethod
    def listar(self) -> List[tuple]:             # [(id, Usuario), ...]
        pass
    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool:
        pass
    @abstractmethod
    def obtener_por_username(self, username: str):  # para JWT login
        pass

class IProyectoRepository(ABC):
    @abstractmethod
    def guardar(self, proyecto) -> tuple:
        """Guarda un proyecto y retorna (id, Proyecto)"""
        pass

    @abstractmethod
    def obtener(self, proyecto_id: int):
        """Busca un proyecto por su ID único"""
        pass

    @abstractmethod
    def listar(self) -> List[tuple]:
        """Retorna una lista de todos los proyectos [(id, Proyecto), ...]"""
        pass

    @abstractmethod
    def eliminar(self, proyecto_id: int) -> bool:
        """Elimina un proyecto por ID. Retorna True si tuvo éxito"""
        pass

class ITareaRepository:
    @abstractmethod
    def guardar(self, tarea) -> tuple:
        """Guarda una tarea y retorna (id, Tarea)"""
        pass

    @abstractmethod
    def obtener(self, tarea_id: int):
        """Busca una tarea por su ID único"""
        pass

    @abstractmethod
    def listar(self) -> List[tuple]:
        """Retorna una lista de todas las tareas [(id, Tarea), ...]"""
        pass

    @abstractmethod
    def eliminar(self, tarea_id: int) -> bool:
        """Elimina una tarea por ID. Retorna True si tuvo éxito"""
        pass