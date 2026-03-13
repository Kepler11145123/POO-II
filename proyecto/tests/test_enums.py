"""
test_enums.py — Tests para PrioridadTarea y EstadoTarea.
"""
import pytest
from src.domain.enums import PrioridadTarea, EstadoTarea


class TestPrioridadTarea:
    """Tests para el enum PrioridadTarea."""

    def test_valores_existentes(self):
        """El enum debe tener exactamente los tres niveles de prioridad."""
        assert PrioridadTarea.BAJA.value  == "Baja"
        assert PrioridadTarea.MEDIA.value == "Media"
        assert PrioridadTarea.ALTA.value  == "Alta"

    def test_cantidad_de_valores(self):
        """Debe haber exactamente 3 prioridades definidas."""
        assert len(PrioridadTarea) == 3

    @pytest.mark.parametrize("prioridad,valor_esperado", [
        (PrioridadTarea.BAJA,  "Baja"),
        (PrioridadTarea.MEDIA, "Media"),
        (PrioridadTarea.ALTA,  "Alta"),
    ])
    def test_valores_parametrizados(self, prioridad, valor_esperado):
        """Cada miembro del enum debe tener el valor de cadena correcto."""
        assert prioridad.value == valor_esperado

    def test_comparacion_entre_miembros(self):
        """Dos referencias al mismo miembro deben ser iguales."""
        assert PrioridadTarea.ALTA == PrioridadTarea.ALTA
        assert PrioridadTarea.ALTA != PrioridadTarea.BAJA

    def test_acceso_por_valor(self):
        """Se debe poder obtener un miembro a partir de su valor string."""
        assert PrioridadTarea("Alta")  == PrioridadTarea.ALTA
        assert PrioridadTarea("Media") == PrioridadTarea.MEDIA
        assert PrioridadTarea("Baja")  == PrioridadTarea.BAJA

    def test_valor_invalido_lanza_excepcion(self):
        """Un valor no registrado debe lanzar ValueError."""
        with pytest.raises(ValueError):
            PrioridadTarea("Crítica")


class TestEstadoTarea:
    """Tests para el enum EstadoTarea."""

    def test_valores_existentes(self):
        """El enum debe tener los tres estados del ciclo de vida de una tarea."""
        assert EstadoTarea.PENDIENTE.value   == "Pendiente"
        assert EstadoTarea.EN_PROGRESO.value == "En Progreso"
        assert EstadoTarea.COMPLETADA.value  == "Completada"

    def test_cantidad_de_valores(self):
        """Debe haber exactamente 3 estados definidos."""
        assert len(EstadoTarea) == 3

    @pytest.mark.parametrize("estado,valor_esperado", [
        (EstadoTarea.PENDIENTE,   "Pendiente"),
        (EstadoTarea.EN_PROGRESO, "En Progreso"),
        (EstadoTarea.COMPLETADA,  "Completada"),
    ])
    def test_valores_parametrizados(self, estado, valor_esperado):
        """Cada estado debe tener el valor de cadena correcto."""
        assert estado.value == valor_esperado

    def test_comparacion_entre_estados(self):
        """Estados distintos no deben ser iguales."""
        assert EstadoTarea.PENDIENTE != EstadoTarea.COMPLETADA

    def test_acceso_por_valor(self):
        """Se debe poder recuperar un estado a partir de su valor string."""
        assert EstadoTarea("Pendiente")   == EstadoTarea.PENDIENTE
        assert EstadoTarea("En Progreso") == EstadoTarea.EN_PROGRESO
        assert EstadoTarea("Completada")  == EstadoTarea.COMPLETADA

    def test_valor_invalido_lanza_excepcion(self):
        """Un valor no registrado debe lanzar ValueError."""
        with pytest.raises(ValueError):
            EstadoTarea("Cancelada")

    def test_enums_son_distintos_entre_si(self):
        """Los miembros de PrioridadTarea y EstadoTarea no deben mezclarse."""
        assert PrioridadTarea.ALTA != EstadoTarea.COMPLETADA
