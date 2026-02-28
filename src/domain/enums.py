from enum import Enum

class PrioridadTarea(Enum):
    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'

class EstadoTarea(Enum):
    PENDIENTE = 'Pendiente'
    EN_PROGRESO = 'En Progreso'
    COMPLETADA = 'Completada'