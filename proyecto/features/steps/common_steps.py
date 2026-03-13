"""
common_steps.py — Pasos Gherkin compartidos entre todos los features.
"""
from behave import given, when, then
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto
from src.domain.enums import PrioridadTarea, EstadoTarea

# Mapa string → enum (usado en múltiples steps)
PRIORIDAD_MAP = {
    "ALTA":  PrioridadTarea.ALTA,
    "MEDIA": PrioridadTarea.MEDIA,
    "BAJA":  PrioridadTarea.BAJA,
}
ESTADO_MAP = {
    "PENDIENTE":   EstadoTarea.PENDIENTE,
    "EN_PROGRESO": EstadoTarea.EN_PROGRESO,
    "COMPLETADA":  EstadoTarea.COMPLETADA,
}


@given("que el sistema está inicializado")
def step_sistema_inicializado(context):
    """Inicializa los diccionarios de estado compartido del contexto."""
    context.usuarios   = {}
    context.proyectos  = {}
    context.tareas     = {}
    context.error      = None
    context.resultado  = None


@given('que existe un usuario con username "{username}" y email "{email}"')
def step_existe_usuario(context, username, email):
    u = Usuario(username, email, f"Nombre {username}")
    context.usuarios[username] = u


@given('el usuario "{username}" está desactivado')
def step_usuario_desactivado(context, username):
    context.usuarios[username].desactivar()


# ── Error genérico compartido ─────────────────────────────────────────────────

@then('debe lanzarse un error de validación con mensaje "{mensaje}"')
def step_error_con_mensaje(context, mensaje):
    assert context.error is not None, "Se esperaba un error pero no se produjo ninguno."
    assert mensaje in str(context.error), (
        f"Mensaje esperado: '{mensaje}'\nMensaje obtenido: '{context.error}'"
    )
