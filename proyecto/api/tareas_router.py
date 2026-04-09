"""
tareas_router.py — Endpoints para operaciones sobre Tarea.

PATCH /tareas/{id}/completar    → marca completada, devuelve item HTML
PATCH /tareas/{id}/prioridad    → cambia prioridad, devuelve item HTML
"""
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from proyecto.api.models import TareaResponse, CambiarPrioridadRequest
from proyecto.src.domain.enums import PrioridadTarea
from proyecto.src.domain.tarea import Tarea
from proyecto.src.infrastructure import repositories

router = APIRouter(prefix="/tareas", tags=["Tareas"])
templates = Jinja2Templates(directory="proyecto/templates")


# ─ Endpoints HTML para HTMX ─

@router.patch(
    "/{tarea_id}/completar",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def completar_tarea_html(tarea_id: int, request: Request):
    """Completa la tarea y devuelve el item HTML actualizado."""
    tarea = repositories.obtener_tarea(tarea_id)
    if not tarea:
        return HTMLResponse("<li>Tarea no encontrada.</li>", status_code=404)
    tarea.completar()
    return templates.TemplateResponse(
        request,
        "tareas/item.html",
        {"tarea": _a_response(tarea_id, tarea)},
    )


@router.patch(
    "/{tarea_id}/prioridad",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def cambiar_prioridad_html(tarea_id: int, request: Request):
    """Cambia la prioridad y devuelve el item HTML actualizado."""
    tarea = repositorio.obtener_tarea(tarea_id)
    if not tarea:
        return HTMLResponse("<li>Tarea no encontrada.</li>", status_code=404)

    form = await request.form()
    prioridad_raw = form.get("prioridad", "").strip()
    try:
        nueva_prioridad = PrioridadTarea(prioridad_raw)
    except ValueError:
        return HTMLResponse("<li>Prioridad inválida.</li>", status_code=422)

    tarea.cambiar_prioridad(nueva_prioridad)
    return templates.TemplateResponse(
        request,
        "tareas/item.html",
        {"tarea": _a_response(tarea_id, tarea)},
    )


# ─ Endpoints JSON (Swagger) ─

@router.patch(
    "/{tarea_id}/completar/json",
    response_model=TareaResponse,
    summary="Completar tarea (JSON)",
)
def completar_tarea_json(tarea_id: int):
    tarea = repositorio.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"Tarea {tarea_id} no encontrada.")
    tarea.completar()
    return _a_response(tarea_id, tarea)


@router.patch(
    "/{tarea_id}/prioridad/json",
    response_model=TareaResponse,
    summary="Cambiar prioridad (JSON)",
)
def cambiar_prioridad_json(tarea_id: int, body: CambiarPrioridadRequest):
    tarea = repositorio.obtener_tarea(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"Tarea {tarea_id} no encontrada.")
    tarea.cambiar_prioridad(body.prioridad)
    return _a_response(tarea_id, tarea)


# ─ Helper ─

def _a_response(tid: int, tarea: Tarea) -> TareaResponse:
    return TareaResponse(
        id=tid,
        titulo=tarea._titulo,
        descripcion=tarea.descripcion,
        estado=tarea._estado,
        prioridad=tarea._prioridad,
        fecha_creacion=tarea.fecha_creacion,
        fecha_completada=tarea._fecha_completada,
    )