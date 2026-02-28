# TaskFlow - Sistema de Gestión de Tareas

Proyecto de modelado orientado a objetos con las entidades principales de un sistema de gestión de tareas.

## Estructura del proyecto
```
src/
└── domain/
    ├── enums.py
    ├── usuario.py
    ├── tarea.py
    └── proyecto.py
test_dominio.py
```

## Requisitos

- Python 3.10+
- pytest
```bash
pip install pytest
```

## Correr los tests

Desde la carpeta raíz del proyecto (`POO II`):
```bash
python -m pytest test_dominio.py -v
```

## Ejemplos de uso
```python
from src.domain.enums import PrioridadTarea, EstadoTarea
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto

# Crear un usuario
usuario = Usuario("juan123", "juan@mail.com", "Juan Pérez")

# Crear un proyecto
proyecto = Proyecto("Mi App", lider=usuario)

# Crear y agregar tareas
tarea = Tarea("Diseñar base de datos", prioridad=PrioridadTarea.ALTA)
proyecto.agregar_tarea(tarea)

# Cambiar estado de una tarea
tarea.iniciar()   # EN_PROGRESO
tarea.completar() # COMPLETADA

# Consultar tareas
pendientes = proyecto.obtener_tareas_pendientes()
altas      = proyecto.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
```