"""
tareas_steps.py — Pasos Gherkin para features/tareas.feature
"""
from behave import given, when, then
from datetime import datetime
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea, EstadoTarea

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


@given('que existe una tarea "{titulo}" con prioridad "{prioridad}"')
def step_existe_tarea(context, titulo, prioridad):
    t = Tarea(titulo, prioridad=PRIORIDAD_MAP[prioridad])
    context.tareas[titulo] = t


# ── When ──────────────────────────────────────────────────────────────────────

@when('creo una tarea con título "{titulo}" y prioridad "{prioridad}"')
def step_crear_tarea(context, titulo, prioridad):
    try:
        t = Tarea(titulo, prioridad=PRIORIDAD_MAP[prioridad])
        context.tareas[titulo] = t
        context.error = None
    except ValueError as e:
        context.error = e


@when('creo una tarea con título "{titulo}" sin descripción ni prioridad')
def step_crear_tarea_minima(context, titulo):
    try:
        t = Tarea(titulo)
        context.tareas[titulo] = t
        context.error = None
    except ValueError as e:
        context.error = e


@when('intento crear una tarea con título "{titulo}"')
def step_intentar_crear_tarea(context, titulo):
    try:
        t = Tarea(titulo)
        context.tareas[titulo] = t
        context.error = None
    except ValueError as e:
        context.error = e


@when('inicio la tarea "{titulo}"')
def step_iniciar_tarea(context, titulo):
    context.tareas[titulo].iniciar()


@when('completo la tarea "{titulo}"')
def step_completar_tarea(context, titulo):
    context.tareas[titulo].completar()


@when('cambio la prioridad de la tarea "{titulo}" a "{nueva_prioridad}"')
def step_cambiar_prioridad(context, titulo, nueva_prioridad):
    context.tareas[titulo].cambiar_prioridad(PRIORIDAD_MAP[nueva_prioridad])


# ── Then ──────────────────────────────────────────────────────────────────────

@then('la tarea debe existir con título "{titulo}"')
def step_tarea_existe(context, titulo):
    assert titulo in context.tareas, f"La tarea '{titulo}' no fue creada."
    assert context.tareas[titulo]._titulo == titulo


@then('la tarea debe estar en estado "{estado}"')
def step_tarea_estado_generico(context, estado):
    t = list(context.tareas.values())[-1]
    assert t._estado == ESTADO_MAP[estado], (
        f"Estado esperado: {estado}, obtenido: {t._estado}"
    )


@then('la tarea "{titulo}" debe estar en estado "{estado}"')
def step_tarea_estado_especifico(context, titulo, estado):
    t = context.tareas[titulo]
    assert t._estado == ESTADO_MAP[estado], (
        f"Estado esperado: {estado}, obtenido: {t._estado}"
    )


@then('la tarea "{titulo}" debe tener fecha de completado registrada')
def step_fecha_completado(context, titulo):
    t = context.tareas[titulo]
    assert t._fecha_completada is not None
    assert isinstance(t._fecha_completada, datetime)


@then('la tarea "{titulo}" debe tener prioridad "{prioridad}"')
def step_tarea_prioridad(context, titulo, prioridad):
    assert context.tareas[titulo]._prioridad == PRIORIDAD_MAP[prioridad]


@then("la prioridad de la tarea debe ser nula")
def step_prioridad_nula(context):
    t = list(context.tareas.values())[-1]
    assert t._prioridad is None
