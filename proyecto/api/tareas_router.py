"""
tareas_router.py — Endpoints para operaciones sobre Tarea.

PATCH /tareas/{id}/completar    → marca una tarea como completada
PATCH /tareas/{id}/prioridad    → cambia la prioridad de una tarea
"""
from fastapi import APIRouter, HTTPException, status
from proyecto.api.models import TareaResponse, CambiarPrioridadRequest
from src.domain.tarea import Tarea
from proyecto.base_de_datos.repositories import repositorio

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.patch(
    "/{tarea_id}/completar",
    response_model=TareaResponse,
    summary="Completar una tarea",
    description="Marca la tarea como COMPLETADA y registra la fecha. "
                "Devuelve 404 si la tarea no existe."
)
def completar_tarea(tarea_id: int):
    tarea = repositorio.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada."
        )
    tarea.completar()
    return _a_response(tarea_id, tarea)


@router.patch(
    "/{tarea_id}/prioridad",
    response_model=TareaResponse,
    summary="Cambiar la prioridad de una tarea",
    description="Actualiza la prioridad de la tarea al valor indicado (Alta, Media, Baja). "
                "Devuelve 404 si la tarea no existe."
)
def cambiar_prioridad(tarea_id: int, body: CambiarPrioridadRequest):
    tarea = repositorio.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {tarea_id} no encontrada."
        )
    tarea.cambiar_prioridad(body.prioridad)
    return _a_response(tarea_id, tarea)


# ── Helper ────────────────────────────────────────────────────────────────────

def _a_response(tid: int, tarea: Tarea) -> TareaResponse:
    return TareaResponse(
        id=tid,
        titulo=tarea._titulo,
        descripcion=tarea.descripcion,
        estado=tarea._estado,
        prioridad=tarea._prioridad,
        fecha_creacion=tarea.fecha_creacion,
        fecha_completada=tarea._fecha_completada
    )
