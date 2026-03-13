"""
usuarios_steps.py — Pasos Gherkin para features/usuarios.feature
"""
from behave import given, when, then
from src.domain.usuario import Usuario


@when('creo un usuario con username "{username}" y email "{email}"')
def step_crear_usuario(context, username, email):
    try:
        u = Usuario(username, email, f"Nombre {username}")
        context.usuarios[username] = u
        context.error = None
    except ValueError as e:
        context.error = e


@when('creo un usuario con username "{username}" y email "{email}" sin nombre completo')
def step_crear_usuario_sin_nombre(context, username, email):
    try:
        u = Usuario(username, email)
        context.usuarios[username] = u
        context.error = None
    except ValueError as e:
        context.error = e


@when('intento crear un usuario con username "{username}" y email "{email}"')
def step_intentar_crear_usuario(context, username, email):
    try:
        u = Usuario(username, email)
        context.usuarios[username] = u
        context.error = None
    except ValueError as e:
        context.error = e


@when('desactivo al usuario "{username}"')
def step_desactivar_usuario(context, username):
    try:
        context.usuarios[username].desactivar()
        context.error = None
    except Exception as e:
        context.error = e


@when('activo al usuario "{username}"')
def step_activar_usuario(context, username):
    try:
        context.usuarios[username].activar()
        context.error = None
    except Exception as e:
        context.error = e


# ── Then ──────────────────────────────────────────────────────────────────────

@then('el usuario debe existir con username "{username}"')
def step_usuario_existe(context, username):
    assert username in context.usuarios, f"Usuario '{username}' no fue creado."
    assert context.usuarios[username].username == username


@then("el usuario debe estar activo")
def step_usuario_activo_generico(context):
    usuario = list(context.usuarios.values())[-1]
    assert usuario._activo is True, "Se esperaba que el usuario estuviera activo."


@then('el usuario "{username}" debe estar activo')
def step_usuario_especifico_activo(context, username):
    assert context.usuarios[username]._activo is True


@then('el usuario "{username}" debe estar inactivo')
def step_usuario_inactivo(context, username):
    assert context.usuarios[username]._activo is False


@then("el nombre completo del usuario debe ser nulo")
def step_nombre_completo_nulo(context):
    usuario = list(context.usuarios.values())[-1]
    assert usuario._nombre_completo is None
