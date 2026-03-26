"""
proyectos_router.py — Endpoints para la entidad Proyecto.

GET  /proyectos                     → lista HTML (HTMX)
POST /proyectos                     → crea proyecto y devuelve lista HTML (HTMX)
GET  /proyectos/{id}                → obtener proyecto JSON
POST /proyectos/{id}/tareas         → crea tarea y devuelve lista tareas HTML (HTMX)
"""
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from proyecto.api.models import ProyectoRequest, ProyectoResponse, TareaRequest, TareaResponse
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.tarea import Tarea
from proyecto.base_de_datos.repositories import repositorio

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])
templates = Jinja2Templates(directory="proyecto/templates")


# ─ Endpoints HTML para HTMX ─

@router.get(
    "",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def listar_proyectos_html(request: Request):
    """Devuelve el partial HTML con la lista de proyectos."""
    proyectos = [_a_response(pid, p) for pid, p in repositorio.listar_proyectos()]
    return templates.TemplateResponse(
        request,
        "proyectos/lista.html",
        {"proyectos": proyectos},
    )


@router.post(
    "",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def crear_proyecto_html(request: Request):
    """Recibe form-data, crea el proyecto y devuelve la lista actualizada."""
    form = await request.form()
    nombre = form.get("nombre", "").strip()
    descripcion = form.get("descripcion", "").strip() or None
    lider_id_raw = form.get("lider_id", "").strip()

    lider = None
    if lider_id_raw:
        try:
            lider = repositorio.obtener_usuario(int(lider_id_raw))
        except ValueError:
            pass

    try:
        proyecto = Proyecto(nombre=nombre, descripcion=descripcion, lider=lider)
    except ValueError as e:
        proyectos = [_a_response(pid, p) for pid, p in repositorio.listar_proyectos()]
        return templates.TemplateResponse(
            request,
            "proyectos/lista.html",
            {"proyectos": proyectos, "error": str(e)},
        )

    repositorio.guardar_proyecto(proyecto)
    proyectos = [_a_response(pid, p) for pid, p in repositorio.listar_proyectos()]
    return templates.TemplateResponse(
        request,
        "proyectos/lista.html",
        {"proyectos": proyectos},
    )


@router.get(
    "/{proyecto_id}/tareas",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def listar_tareas_html(proyecto_id: int, request: Request):
    """Devuelve el partial HTML con las tareas de un proyecto."""
    proyecto = repositorio.obtener_proyecto(proyecto_id)
    if not proyecto:
        return HTMLResponse("<p>Proyecto no encontrado.</p>", status_code=404)

    tareas = [
        _a_response_tarea(tid, t)
        for tid, t in repositorio.listar_tareas()
        if t in proyecto.tareas
    ]
    return templates.TemplateResponse(
        request,
        "tareas/lista.html",
        {"tareas": tareas, "proyecto_id": proyecto_id},
    )


@router.post(
    "/{proyecto_id}/tareas",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def agregar_tarea_html(proyecto_id: int, request: Request):
    """Recibe form-data, crea la tarea y devuelve la lista de tareas actualizada."""
    from proyecto.src.domain.enums import PrioridadTarea

    proyecto = repositorio.obtener_proyecto(proyecto_id)
    if not proyecto:
        return HTMLResponse("<p>Proyecto no encontrado.</p>", status_code=404)

    form = await request.form()
    titulo = form.get("titulo", "").strip()
    descripcion = form.get("descripcion", "").strip() or None
    prioridad_raw = form.get("prioridad", "").strip()

    prioridad = None
    if prioridad_raw:
        try:
            prioridad = PrioridadTarea(prioridad_raw.capitalize())
        except ValueError:
            pass

    try:
        tarea = Tarea(titulo=titulo, descripcion=descripcion, prioridad=prioridad)
        proyecto.agregar_tarea(tarea)
        repositorio.guardar_tarea(tarea)
    except ValueError as e:
        tareas = [
            _a_response_tarea(tid, t)
            for tid, t in repositorio.listar_tareas()
            if t in proyecto.tareas
        ]
        return templates.TemplateResponse(
            request,
            "tareas/lista.html",
            {"tareas": tareas, "proyecto_id": proyecto_id, "error": str(e)},
        )

    tareas = [
        _a_response_tarea(tid, t)
        for tid, t in repositorio.listar_tareas()
        if t in proyecto.tareas
    ]
    return templates.TemplateResponse(
        request,
        "tareas/lista.html",
        {"tareas": tareas, "proyecto_id": proyecto_id},
    )


# ─ Endpoints JSON (para Swagger / API pura) ─

@router.get(
    "/json",
    response_model=list[ProyectoResponse],
    summary="Listar proyectos (JSON)",
)
def listar_proyectos_json():
    return [_a_response(pid, p) for pid, p in repositorio.listar_proyectos()]


@router.get(
    "/{proyecto_id}/json",
    response_model=ProyectoResponse,
    summary="Obtener proyecto por ID (JSON)",
)
def obtener_proyecto_json(proyecto_id: int):
    proyecto = repositorio.obtener_proyecto(proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail=f"Proyecto {proyecto_id} no encontrado.")
    return _a_response(proyecto_id, proyecto)


# ─ Helpers ─

def _a_response(pid: int, proyecto: Proyecto) -> ProyectoResponse:
    lider_id = None
    if proyecto.lider:
        for uid, u in repositorio.listar_usuarios():
            if u is proyecto.lider:
                lider_id = uid
                break
    return ProyectoResponse(
        id=pid,
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        lider_id=lider_id,
        total_tareas=len(proyecto.tareas),
        fecha_creacion=proyecto.fecha_creacion,
    )


def _a_response_tarea(tid: int, tarea: Tarea) -> TareaResponse:
    return TareaResponse(
        id=tid,
        titulo=tarea._titulo,
        descripcion=tarea.descripcion,
        estado=tarea._estado,
        prioridad=tarea._prioridad,
        fecha_creacion=tarea.fecha_creacion,
        fecha_completada=tarea._fecha_completada,
    )