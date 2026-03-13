"""
test_tarea.py — Tests exhaustivos para la clase Tarea.
Cubre: creación, cambiar estado, cambiar prioridad, completar.
"""
import pytest
from datetime import datetime
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea, EstadoTarea


class TestTareaCreacion:
    """Tests del constructor y valores iniciales de Tarea."""

    def test_creacion_valida_con_todos_los_campos(self):
        """Una tarea con título válido debe crearse con los valores correctos."""
        t = Tarea("Diseñar BD", descripcion="Modelo ER", prioridad=PrioridadTarea.ALTA)
        assert t._titulo          == "Diseñar BD"
        assert t.descripcion      == "Modelo ER"
        assert t._prioridad       == PrioridadTarea.ALTA
        assert t._estado          == EstadoTarea.PENDIENTE
        assert t._fecha_completada is None

    def test_estado_inicial_es_pendiente(self, tarea_ejemplo):
        """Toda tarea recién creada debe tener estado PENDIENTE."""
        assert tarea_ejemplo._estado == EstadoTarea.PENDIENTE

    def test_fecha_completada_inicial_es_none(self, tarea_ejemplo):
        """Una tarea nueva no debe tener fecha de completado."""
        assert tarea_ejemplo._fecha_completada is None

    def test_fecha_creacion_asignada(self, tarea_ejemplo):
        """La fecha de creación debe quedar registrada."""
        assert isinstance(tarea_ejemplo.fecha_creacion, datetime)

    def test_creacion_sin_descripcion_ni_prioridad(self):
        """Título mínimo válido sin campos opcionales debe funcionar."""
        t = Tarea("Fix bug")
        assert t._titulo    == "Fix bug"
        assert t.descripcion is None
        assert t._prioridad  is None

    @pytest.mark.parametrize("titulo_invalido", [
        "AB",   # exactamente 2 chars
        "A",    # 1 char
        "",     # vacío
    ])
    def test_titulo_demasiado_corto_lanza_error(self, titulo_invalido):
        """Un título con menos de 3 caracteres debe lanzar ValueError."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Tarea(titulo_invalido)

    def test_titulo_exactamente_tres_caracteres_es_valido(self):
        """Un título de exactamente 3 caracteres debe ser válido."""
        t = Tarea("ABC")
        assert t._titulo == "ABC"


class TestTareaCambiarEstado:
    """Tests de las transiciones de estado."""

    def test_iniciar_cambia_estado_a_en_progreso(self, tarea_ejemplo):
        """iniciar() debe cambiar el estado a EN_PROGRESO."""
        tarea_ejemplo.iniciar()
        assert tarea_ejemplo._estado == EstadoTarea.EN_PROGRESO

    def test_completar_cambia_estado_a_completada(self, tarea_ejemplo):
        """completar() debe cambiar el estado a COMPLETADA."""
        tarea_ejemplo.completar()
        assert tarea_ejemplo._estado == EstadoTarea.COMPLETADA

    def test_completar_registra_fecha_completada(self, tarea_ejemplo):
        """completar() debe registrar la fecha y hora del momento."""
        before = datetime.now()
        tarea_ejemplo.completar()
        after = datetime.now()
        assert tarea_ejemplo._fecha_completada is not None
        assert before <= tarea_ejemplo._fecha_completada <= after

    def test_flujo_pendiente_en_progreso_completada(self):
        """Una tarea debe poder recorrer el ciclo completo de estados."""
        t = Tarea("Ciclo completo", prioridad=PrioridadTarea.MEDIA)
        assert t._estado == EstadoTarea.PENDIENTE
        t.iniciar()
        assert t._estado == EstadoTarea.EN_PROGRESO
        t.completar()
        assert t._estado == EstadoTarea.COMPLETADA

    def test_completar_desde_pendiente_sin_iniciar(self):
        """Completar directamente desde PENDIENTE debe ser permitido."""
        t = Tarea("Directa", prioridad=PrioridadTarea.BAJA)
        t.completar()
        assert t._estado == EstadoTarea.COMPLETADA


class TestTareaCambiarPrioridad:
    """Tests de cambio de prioridad."""

    @pytest.mark.parametrize("nueva_prioridad", [
        PrioridadTarea.ALTA,
        PrioridadTarea.MEDIA,
        PrioridadTarea.BAJA,
    ])
    def test_cambiar_a_cualquier_prioridad(self, nueva_prioridad):
        """Debe ser posible cambiar a cualquiera de los tres niveles."""
        t = Tarea("Tarea prueba", prioridad=PrioridadTarea.ALTA)
        t.cambiar_prioridad(nueva_prioridad)
        assert t._prioridad == nueva_prioridad

    def test_cambiar_prioridad_no_altera_estado(self, tarea_ejemplo):
        """Cambiar la prioridad no debe modificar el estado de la tarea."""
        estado_original = tarea_ejemplo._estado
        tarea_ejemplo.cambiar_prioridad(PrioridadTarea.BAJA)
        assert tarea_ejemplo._estado == estado_original

    def test_cambiar_prioridad_multiples_veces(self):
        """La prioridad debe poder cambiarse más de una vez."""
        t = Tarea("Iterativa", prioridad=PrioridadTarea.BAJA)
        t.cambiar_prioridad(PrioridadTarea.MEDIA)
        assert t._prioridad == PrioridadTarea.MEDIA
        t.cambiar_prioridad(PrioridadTarea.ALTA)
        assert t._prioridad == PrioridadTarea.ALTA


class TestTareaCompletar:
    """Tests específicos del método completar()."""

    def test_completar_establece_estado_correcto(self, tarea_ejemplo):
        """El estado tras completar() debe ser COMPLETADA."""
        tarea_ejemplo.completar()
        assert tarea_ejemplo._estado == EstadoTarea.COMPLETADA

    def test_completar_establece_fecha(self, tarea_ejemplo):
        """La fecha_completada debe ser un datetime tras completar()."""
        tarea_ejemplo.completar()
        assert isinstance(tarea_ejemplo._fecha_completada, datetime)

    def test_completar_no_borra_titulo_ni_prioridad(self, tarea_ejemplo):
        """completar() no debe alterar el título ni la prioridad."""
        titulo_original    = tarea_ejemplo._titulo
        prioridad_original = tarea_ejemplo._prioridad
        tarea_ejemplo.completar()
        assert tarea_ejemplo._titulo    == titulo_original
        assert tarea_ejemplo._prioridad == prioridad_original
