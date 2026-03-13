"""
conftest.py — Fixtures globales reutilizables para pytest.
Disponibles automáticamente en todos los archivos de test.
"""
import pytest
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto
from src.domain.enums import PrioridadTarea, EstadoTarea


# ── Scope: module — datos de solo lectura compartidos en el módulo ─────────────

@pytest.fixture(scope="module")
def usuario_ejemplo():
    """Usuario válido para pruebas (solo lectura — scope module)."""
    return Usuario("juan123", "juan@example.com", "Juan Pérez")


@pytest.fixture(scope="module")
def proyecto_ejemplo(usuario_ejemplo):
    """Proyecto con líder válido (solo lectura — scope module)."""
    return Proyecto("Sistema de Gestión", descripcion="Proyecto de prueba", lider=usuario_ejemplo)


# ── Scope: function — objetos frescos por test (modifican estado) ─────────────

@pytest.fixture
def tarea_ejemplo():
    """Tarea pendiente con prioridad ALTA (scope function — estado mutable)."""
    return Tarea("Diseñar base de datos", descripcion="Modelo entidad-relación", prioridad=PrioridadTarea.ALTA)


@pytest.fixture
def usuario_fresco():
    """Usuario nuevo por cada test (para tests que modifican estado)."""
    return Usuario("maria99", "maria@example.com", "María García")


@pytest.fixture
def proyecto_fresco(usuario_fresco):
    """Proyecto nuevo por cada test (para tests que agregan/modifican tareas)."""
    return Proyecto("Proyecto Fresco", descripcion="Para tests con estado", lider=usuario_fresco)


@pytest.fixture
def proyecto_con_tareas(proyecto_fresco):
    """Proyecto poblado con tareas en distintos estados y prioridades."""
    t1 = Tarea("Tarea alta pendiente",   prioridad=PrioridadTarea.ALTA)
    t2 = Tarea("Tarea media en progreso", prioridad=PrioridadTarea.MEDIA)
    t3 = Tarea("Tarea baja completada",  prioridad=PrioridadTarea.BAJA)
    t4 = Tarea("Tarea alta completada",  prioridad=PrioridadTarea.ALTA)

    t2.iniciar()
    t3.completar()
    t4.completar()

    proyecto_fresco.agregar_tarea(t1)
    proyecto_fresco.agregar_tarea(t2)
    proyecto_fresco.agregar_tarea(t3)
    proyecto_fresco.agregar_tarea(t4)

    return proyecto_fresco
