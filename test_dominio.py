import pytest
from src.domain.enums import PrioridadTarea, EstadoTarea
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def usuario():
    return Usuario("juan123", "juan@example.com", "Juan Pérez")

@pytest.fixture
def tarea():
    return Tarea("Diseñar BD", prioridad=PrioridadTarea.ALTA)

@pytest.fixture
def proyecto(usuario):
    return Proyecto("Mi Proyecto", lider=usuario)


# ── Tests Usuario ─────────────────────────────────────────────────────────────

def test_usuario_creacion(usuario):
    assert usuario.username == "juan123"
    assert usuario.email == "juan@example.com"
    assert usuario._activo is True

def test_usuario_username_corto():
    with pytest.raises(ValueError):
        Usuario("ab", "ab@mail.com")

def test_usuario_username_no_alfanumerico():
    with pytest.raises(ValueError):
        Usuario("ab_cd", "ab@mail.com")

def test_usuario_email_invalido():
    with pytest.raises(ValueError):
        Usuario("abc123", "correo_invalido")

def test_usuario_activar_desactivar(usuario):
    usuario.desactivar()
    assert usuario._activo is False
    usuario.activar()
    assert usuario._activo is True

def test_usuario_str(usuario):
    assert str(usuario) == "@juan123"

def test_usuario_repr(usuario):
    assert repr(usuario) == "Usuario('juan123', 'juan@example.com')"


# ── Tests Tarea ───────────────────────────────────────────────────────────────

def test_tarea_creacion(tarea):
    assert tarea._titulo == "Diseñar BD"
    assert tarea._estado == EstadoTarea.PENDIENTE
    assert tarea._fecha_completada is None

def test_tarea_titulo_corto():
    with pytest.raises(ValueError):
        Tarea("AB")

def test_tarea_iniciar(tarea):
    tarea.iniciar()
    assert tarea._estado == EstadoTarea.EN_PROGRESO

def test_tarea_completar(tarea):
    tarea.completar()
    assert tarea._estado == EstadoTarea.COMPLETADA
    assert tarea._fecha_completada is not None

def test_tarea_cambiar_prioridad(tarea):
    tarea.cambiar_prioridad(PrioridadTarea.BAJA)
    assert tarea._prioridad == PrioridadTarea.BAJA


# ── Tests Proyecto ────────────────────────────────────────────────────────────

def test_proyecto_creacion(proyecto, usuario):
    assert proyecto.nombre == "Mi Proyecto"
    assert proyecto.lider == usuario
    assert proyecto.tareas == []

def test_proyecto_nombre_corto(usuario):
    with pytest.raises(ValueError):
        Proyecto("AB", lider=usuario)

def test_proyecto_agregar_tarea(proyecto, tarea):
    proyecto.agregar_tarea(tarea)
    assert tarea in proyecto.tareas

def test_proyecto_agregar_objeto_invalido(proyecto):
    with pytest.raises(ValueError):
        proyecto.agregar_tarea("no soy una tarea")

def test_proyecto_tareas_pendientes(proyecto):
    t1 = Tarea("Tarea pendiente", prioridad=PrioridadTarea.MEDIA)
    t2 = Tarea("Tarea completada", prioridad=PrioridadTarea.BAJA)
    t2.completar()
    proyecto.agregar_tarea(t1)
    proyecto.agregar_tarea(t2)
    pendientes = proyecto.obtener_tareas_pendientes()
    assert t1 in pendientes
    assert t2 not in pendientes

def test_proyecto_tareas_por_prioridad(proyecto):
    t_alta = Tarea("Alta", prioridad=PrioridadTarea.ALTA)
    t_baja = Tarea("Baja", prioridad=PrioridadTarea.BAJA)
    proyecto.agregar_tarea(t_alta)
    proyecto.agregar_tarea(t_baja)
    resultado = proyecto.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
    assert t_alta in resultado
    assert t_baja not in resultado