"""
test_proyecto.py — Tests exhaustivos para la clase Proyecto.
Cubre: creación, agregar tarea, tareas pendientes, filtrar por prioridad.
"""
import pytest
from src.domain.proyecto import Proyecto
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.enums import PrioridadTarea, EstadoTarea


class TestProyectoCreacion:
    """Tests del constructor y atributos iniciales."""

    def test_creacion_valida_con_lider(self, proyecto_fresco, usuario_fresco):
        """Un proyecto con nombre y líder válidos debe crearse correctamente."""
        assert proyecto_fresco.nombre == "Proyecto Fresco"
        assert proyecto_fresco.lider  == usuario_fresco
        assert proyecto_fresco.tareas == []

    def test_creacion_sin_lider(self):
        """Un proyecto puede crearse sin líder asignado."""
        p = Proyecto("Sin Líder")
        assert p.lider is None

    def test_creacion_con_descripcion(self):
        """La descripción debe quedar almacenada correctamente."""
        p = Proyecto("Proyecto X", descripcion="Desc de prueba")
        assert p.descripcion == "Desc de prueba"

    def test_lista_tareas_inicia_vacia(self, proyecto_fresco):
        """Un proyecto nuevo debe tener la lista de tareas vacía."""
        assert len(proyecto_fresco.tareas) == 0

    def test_str_con_lider(self, proyecto_fresco):
        """__str__ debe incluir el nombre del proyecto y del líder."""
        resultado = str(proyecto_fresco)
        assert "Proyecto Fresco" in resultado
        assert "María García" in resultado

    def test_str_sin_lider(self):
        """__str__ sin líder debe indicar 'Sin líder'."""
        p = Proyecto("Sin Lider")
        assert "Sin líder" in str(p)

    @pytest.mark.parametrize("nombre_invalido", [
        "AB",  # 2 chars
        "A",   # 1 char
        "",    # vacío
    ])
    def test_nombre_demasiado_corto_lanza_error(self, nombre_invalido, usuario_fresco):
        """Un nombre con menos de 3 caracteres debe lanzar ValueError."""
        with pytest.raises(ValueError, match="al menos 3 caracteres"):
            Proyecto(nombre_invalido, lider=usuario_fresco)

    def test_lider_invalido_lanza_error(self):
        """Pasar un objeto no-Usuario como líder debe lanzar ValueError."""
        with pytest.raises(ValueError, match="usuario válido"):
            Proyecto("Proyecto X", lider="no soy usuario")


class TestProyectoAgregarTarea:
    """Tests del método agregar_tarea()."""

    def test_agregar_tarea_valida(self, proyecto_fresco, tarea_ejemplo):
        """Una Tarea válida debe añadirse a la lista de tareas."""
        proyecto_fresco.agregar_tarea(tarea_ejemplo)
        assert tarea_ejemplo in proyecto_fresco.tareas

    def test_agregar_multiples_tareas(self, proyecto_fresco):
        """Deben poder agregarse varias tareas sin error."""
        t1 = Tarea("Tarea uno",  prioridad=PrioridadTarea.ALTA)
        t2 = Tarea("Tarea dos",  prioridad=PrioridadTarea.MEDIA)
        t3 = Tarea("Tarea tres", prioridad=PrioridadTarea.BAJA)
        proyecto_fresco.agregar_tarea(t1)
        proyecto_fresco.agregar_tarea(t2)
        proyecto_fresco.agregar_tarea(t3)
        assert len(proyecto_fresco.tareas) == 3

    @pytest.mark.parametrize("objeto_invalido", [
        "cadena de texto",
        42,
        None,
        {"clave": "valor"},
        ["lista"],
    ])
    def test_agregar_objeto_no_tarea_lanza_error(self, proyecto_fresco, objeto_invalido):
        """Solo objetos Tarea pueden agregarse; cualquier otro tipo lanza ValueError."""
        with pytest.raises(ValueError, match="tipo Tarea"):
            proyecto_fresco.agregar_tarea(objeto_invalido)

    def test_agregar_tarea_no_duplica_otras(self, proyecto_fresco, tarea_ejemplo):
        """Agregar una tarea no debe modificar las tareas ya existentes."""
        t_previa = Tarea("Tarea previa", prioridad=PrioridadTarea.MEDIA)
        proyecto_fresco.agregar_tarea(t_previa)
        proyecto_fresco.agregar_tarea(tarea_ejemplo)
        assert t_previa    in proyecto_fresco.tareas
        assert tarea_ejemplo in proyecto_fresco.tareas


class TestProyectoTareasPendientes:
    """Tests de obtener_tareas_pendientes()."""

    def test_solo_retorna_pendientes(self, proyecto_con_tareas):
        """Debe retornar únicamente tareas en estado PENDIENTE."""
        pendientes = proyecto_con_tareas.obtener_tareas_pendientes()
        for t in pendientes:
            assert t._estado == EstadoTarea.PENDIENTE

    def test_no_incluye_completadas(self, proyecto_con_tareas):
        """Las tareas completadas no deben aparecer en pendientes."""
        pendientes = proyecto_con_tareas.obtener_tareas_pendientes()
        for t in pendientes:
            assert t._estado != EstadoTarea.COMPLETADA

    def test_no_incluye_en_progreso(self, proyecto_con_tareas):
        """Las tareas en progreso no deben aparecer en pendientes."""
        pendientes = proyecto_con_tareas.obtener_tareas_pendientes()
        for t in pendientes:
            assert t._estado != EstadoTarea.EN_PROGRESO

    def test_proyecto_sin_tareas_retorna_lista_vacia(self, proyecto_fresco):
        """Un proyecto sin tareas debe retornar lista vacía."""
        assert proyecto_fresco.obtener_tareas_pendientes() == []

    def test_todas_completadas_retorna_lista_vacia(self, proyecto_fresco):
        """Si todas las tareas están completadas, pendientes debe ser []."""
        t = Tarea("Completa", prioridad=PrioridadTarea.ALTA)
        t.completar()
        proyecto_fresco.agregar_tarea(t)
        assert proyecto_fresco.obtener_tareas_pendientes() == []


class TestProyectoFiltrarPorPrioridad:
    """Tests de obtener_tareas_por_prioridad()."""

    @pytest.mark.parametrize("prioridad", [
        PrioridadTarea.ALTA,
        PrioridadTarea.MEDIA,
        PrioridadTarea.BAJA,
    ])
    def test_filtrar_retorna_solo_la_prioridad_indicada(self, proyecto_con_tareas, prioridad):
        """Solo deben retornarse tareas que coincidan con la prioridad dada."""
        resultado = proyecto_con_tareas.obtener_tareas_por_prioridad(prioridad)
        for t in resultado:
            assert t._prioridad == prioridad

    def test_filtrar_prioridad_sin_coincidencias_retorna_vacio(self, proyecto_fresco):
        """Si no hay tareas de esa prioridad, debe retornar lista vacía."""
        t = Tarea("Solo media", prioridad=PrioridadTarea.MEDIA)
        proyecto_fresco.agregar_tarea(t)
        resultado = proyecto_fresco.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
        assert resultado == []

    def test_filtrar_incluye_tareas_de_cualquier_estado(self, proyecto_fresco):
        """El filtro por prioridad no debe discriminar por estado."""
        t_pend = Tarea("Alta pendiente",   prioridad=PrioridadTarea.ALTA)
        t_comp = Tarea("Alta completada",  prioridad=PrioridadTarea.ALTA)
        t_comp.completar()
        proyecto_fresco.agregar_tarea(t_pend)
        proyecto_fresco.agregar_tarea(t_comp)
        resultado = proyecto_fresco.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
        assert t_pend in resultado
        assert t_comp in resultado
