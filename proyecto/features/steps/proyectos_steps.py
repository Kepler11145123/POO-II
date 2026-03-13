"""
proyectos_steps.py — Pasos Gherkin para features/proyectos.feature
"""
from behave import given, when, then
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea

PRIORIDAD_MAP = {
    "ALTA":  PrioridadTarea.ALTA,
    "MEDIA": PrioridadTarea.MEDIA,
    "BAJA":  PrioridadTarea.BAJA,
}


@given('que existe el proyecto "{nombre}" con el líder "{username}"')
def step_existe_proyecto(context, nombre, username):
    lider = context.usuarios[username]
    p = Proyecto(nombre, lider=lider)
    context.proyectos[nombre] = p


@given('el proyecto "{nombre}" tiene una tarea "{titulo}" con prioridad "{prioridad}"')
def step_proyecto_con_tarea(context, nombre, titulo, prioridad):
    t = Tarea(titulo, prioridad=PRIORIDAD_MAP[prioridad])
    context.proyectos[nombre].agregar_tarea(t)
    context.tareas[titulo] = t


@given('el proyecto "{nombre}" tiene una tarea completada "{titulo}"')
def step_proyecto_con_tarea_completada(context, nombre, titulo):
    t = Tarea(titulo, prioridad=PrioridadTarea.BAJA)
    t.completar()
    context.proyectos[nombre].agregar_tarea(t)
    context.tareas[titulo] = t


# ── When ──────────────────────────────────────────────────────────────────────

@when('creo un proyecto llamado "{nombre}" con el líder "{username}"')
def step_crear_proyecto_con_lider(context, nombre, username):
    try:
        lider = context.usuarios[username]
        p = Proyecto(nombre, lider=lider)
        context.proyectos[nombre] = p
        context.error = None
    except ValueError as e:
        context.error = e


@when('creo un proyecto llamado "{nombre}" sin líder')
def step_crear_proyecto_sin_lider(context, nombre):
    try:
        p = Proyecto(nombre)
        context.proyectos[nombre] = p
        context.error = None
    except ValueError as e:
        context.error = e


@when('intento crear un proyecto con nombre "{nombre}" y el líder "{username}"')
def step_intentar_crear_proyecto(context, nombre, username):
    try:
        lider = context.usuarios[username]
        p = Proyecto(nombre, lider=lider)
        context.proyectos[nombre] = p
        context.error = None
    except ValueError as e:
        context.error = e


@when('agrego la tarea "{titulo}" con prioridad "{prioridad}" al proyecto "{nombre}"')
def step_agregar_tarea_a_proyecto(context, titulo, prioridad, nombre):
    try:
        t = Tarea(titulo, prioridad=PRIORIDAD_MAP[prioridad])
        context.proyectos[nombre].agregar_tarea(t)
        context.tareas[titulo] = t
        context.error = None
    except ValueError as e:
        context.error = e


@when('intento agregar "{objeto}" al proyecto "{nombre}"')
def step_agregar_invalido(context, objeto, nombre):
    try:
        context.proyectos[nombre].agregar_tarea(objeto)
        context.error = None
    except ValueError as e:
        context.error = e


@when('consulto las tareas pendientes del proyecto "{nombre}"')
def step_consultar_pendientes(context, nombre):
    context.resultado = context.proyectos[nombre].obtener_tareas_pendientes()


@when('filtro las tareas del proyecto "{nombre}" por prioridad "{prioridad}"')
def step_filtrar_por_prioridad(context, nombre, prioridad):
    context.resultado = context.proyectos[nombre].obtener_tareas_por_prioridad(
        PRIORIDAD_MAP[prioridad]
    )


# ── Then ──────────────────────────────────────────────────────────────────────

@then('el proyecto "{nombre}" debe existir')
def step_proyecto_existe(context, nombre):
    assert nombre in context.proyectos, f"Proyecto '{nombre}' no fue creado."


@then('el proyecto debe tener 0 tareas')
def step_proyecto_sin_tareas(context):
    p = list(context.proyectos.values())[-1]
    assert len(p.tareas) == 0


@then('el proyecto "{nombre}" debe tener {cantidad:d} tarea')
def step_proyecto_con_n_tareas(context, nombre, cantidad):
    assert len(context.proyectos[nombre].tareas) == cantidad


@then('debo obtener {cantidad:d} tarea pendiente')
def step_n_tareas_pendientes(context, cantidad):
    assert len(context.resultado) == cantidad


@then('debo obtener {cantidad:d} tarea con prioridad "{prioridad}"')
def step_n_tareas_con_prioridad(context, cantidad, prioridad):
    assert len(context.resultado) == cantidad
    for t in context.resultado:
        assert t._prioridad == PRIORIDAD_MAP[prioridad]


@then("el líder del proyecto debe ser nulo")
def step_lider_nulo(context):
    p = list(context.proyectos.values())[-1]
    assert p.lider is None
