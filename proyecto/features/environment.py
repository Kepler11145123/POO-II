"""
environment.py — Hooks globales de behave.
Se ejecutan antes/después de cada escenario para garantizar estado limpio.
"""


def before_scenario(context, scenario):
    """Reinicia el estado compartido antes de cada escenario."""
    context.usuarios  = {}
    context.proyectos = {}
    context.tareas    = {}
    context.error     = None
    context.resultado = None
