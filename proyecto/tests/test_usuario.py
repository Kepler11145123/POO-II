"""
test_usuario.py — Tests exhaustivos para la clase Usuario.
Cubre: creación válida, username inválido, email inválido, activar/desactivar.
"""
import pytest
from datetime import datetime
from src.domain.usuario import Usuario


class TestUsuarioCreacion:
    """Tests del constructor y atributos iniciales."""

    def test_creacion_valida_con_todos_los_campos(self, usuario_ejemplo):
        """Un usuario con datos válidos debe crearse correctamente."""
        assert usuario_ejemplo.username        == "juan123"
        assert usuario_ejemplo.email           == "juan@example.com"
        assert usuario_ejemplo._nombre_completo == "Juan Pérez"
        assert usuario_ejemplo._activo         is True

    def test_activo_por_defecto_al_crear(self, usuario_ejemplo):
        """Todo usuario nuevo debe estar activo al crearse."""
        assert usuario_ejemplo._activo is True

    def test_fecha_registro_asignada(self, usuario_ejemplo):
        """La fecha de registro debe quedar registrada al crear el usuario."""
        assert isinstance(usuario_ejemplo.fecha_registro, datetime)

    def test_creacion_sin_nombre_completo(self):
        """El nombre completo es opcional; debe poder omitirse."""
        u = Usuario("pedro99", "pedro@mail.com")
        assert u._nombre_completo is None

    def test_str_devuelve_arroba_username(self, usuario_ejemplo):
        """__str__ debe devolver '@username'."""
        assert str(usuario_ejemplo) == "@juan123"

    def test_repr_formato_correcto(self, usuario_ejemplo):
        """__repr__ debe devolver el formato Usuario('username', 'email')."""
        assert repr(usuario_ejemplo) == "Usuario('juan123', 'juan@example.com')"


class TestUsuarioUsernameInvalido:
    """Tests de validación del campo username."""

    @pytest.mark.parametrize("username_invalido", [
        "ab",       # demasiado corto
        "a",        # un solo caracter
        "",         # vacío
    ])
    def test_username_demasiado_corto_lanza_error(self, username_invalido):
        """Un username con menos de 3 caracteres debe lanzar ValueError."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Usuario(username_invalido, "test@mail.com")

    @pytest.mark.parametrize("username_invalido", [
        "ab_cd",    # guion bajo
        "user name",# espacio
        "user@1",   # arroba
        "abc-def",  # guion
        "abc.def",  # punto
    ])
    def test_username_no_alfanumerico_lanza_error(self, username_invalido):
        """Un username con caracteres no alfanuméricos debe lanzar ValueError."""
        with pytest.raises(ValueError, match="letras y números"):
            Usuario(username_invalido, "test@mail.com")

    def test_username_valido_solo_letras(self):
        """Un username con solo letras debe ser válido."""
        u = Usuario("pedro", "pedro@mail.com")
        assert u.username == "pedro"

    def test_username_valido_solo_numeros(self):
        """Un username con solo números debe ser válido si tiene 3+ chars."""
        u = Usuario("123", "num@mail.com")
        assert u.username == "123"

    def test_username_valido_alfanumerico(self):
        """Un username alfanumérico mixto debe ser válido."""
        u = Usuario("user99", "u@mail.com")
        assert u.username == "user99"


class TestUsuarioEmailInvalido:
    """Tests de validación del campo email."""

    @pytest.mark.parametrize("email_invalido", [
        "sinArroba.com",     # sin @
        "sin_punto@dominio", # sin punto
        "invalido",          # texto plano
        "@.com",             # solo @ y punto
    ])
    def test_email_invalido_lanza_error(self, email_invalido):
        """Emails sin @ o sin punto deben lanzar ValueError."""
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario("validuser", email_invalido)

    @pytest.mark.parametrize("email_valido", [
        "user@mail.com",
        "nombre.apellido@empresa.co",
        "test+tag@correo.org",
        "a@b.co",
    ])
    def test_emails_validos_aceptados(self, email_valido):
        """Emails con @ y punto deben ser aceptados."""
        u = Usuario("usertest", email_valido)
        assert u.email == email_valido

    def test_cambiar_email_valido(self):
        """El setter de email debe permitir actualizar con un valor válido."""
        u = Usuario("usertest", "original@mail.com")
        u.email = "nuevo@mail.com"
        assert u.email == "nuevo@mail.com"

    def test_cambiar_email_invalido_lanza_error(self):
        """El setter de email debe rechazar valores inválidos."""
        u = Usuario("usertest", "original@mail.com")
        with pytest.raises(ValueError):
            u.email = "no-es-email"


class TestUsuarioActivarDesactivar:
    """Tests del ciclo activo/inactivo del usuario."""

    def test_desactivar_usuario_activo(self, usuario_fresco):
        """Desactivar un usuario activo debe poner _activo en False."""
        usuario_fresco.desactivar()
        assert usuario_fresco._activo is False

    def test_activar_usuario_inactivo(self, usuario_fresco):
        """Activar un usuario inactivo debe poner _activo en True."""
        usuario_fresco.desactivar()
        usuario_fresco.activar()
        assert usuario_fresco._activo is True

    def test_desactivar_dos_veces_sigue_inactivo(self, usuario_fresco):
        """Desactivar un usuario ya inactivo no debe lanzar error."""
        usuario_fresco.desactivar()
        usuario_fresco.desactivar()
        assert usuario_fresco._activo is False

    def test_activar_dos_veces_sigue_activo(self, usuario_fresco):
        """Activar un usuario ya activo no debe lanzar error."""
        usuario_fresco.activar()
        usuario_fresco.activar()
        assert usuario_fresco._activo is True

    def test_ciclo_completo_activar_desactivar(self, usuario_fresco):
        """El usuario debe poder alternar entre activo e inactivo múltiples veces."""
        assert usuario_fresco._activo is True
        usuario_fresco.desactivar()
        assert usuario_fresco._activo is False
        usuario_fresco.activar()
        assert usuario_fresco._activo is True
