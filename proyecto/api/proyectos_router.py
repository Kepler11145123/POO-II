"""
proyectos_router.py — Endpoints para la entidad Proyecto.

GET  /proyectos                     → listar todos los proyectos
POST /proyectos                     → crear un nuevo proyecto
GET  /proyectos/{id}                → obtener un proyecto por ID
POST /proyectos/{id}/tareas         → agregar una tarea a un proyecto
"""
from fastapi import APIRouter, HTTPException, status
from proyecto.api.models import ProyectoRequest, ProyectoResponse, TareaRequest, TareaResponse
from src.domain.proyecto import Proyecto
from src.domain.tarea import Tarea
from proyecto.base_de_datos.repositories import repositorio

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.get(
    "/",
    response_model=list[ProyectoResponse],
    summary="Listar todos los proyectos",
    description="Devuelve todos los proyectos registrados con su cantidad de tareas."
)
def listar_proyectos():
    return [_a_response(pid, proyecto) for pid, proyecto in repositorio.listar_proyectos()]


@router.post(
    "/",
    response_model=ProyectoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo proyecto",
    description="Crea un proyecto. Si se proporciona `lider_id`, el usuario debe existir. "
                "Devuelve 404 si el líder no existe, 422 si el nombre es inválido."
)
def crear_proyecto(body: ProyectoRequest):
    lider = None
    if body.lider_id is not None:
        lider = repositorio.obtener_usuario(body.lider_id)
        if not lider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {body.lider_id} no encontrado."
            )
    try:
        proyecto = Proyecto(
            nombre=body.nombre,
            descripcion=body.descripcion,
            lider=lider
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    pid = repositorio.guardar_proyecto(proyecto)
    return _a_response(pid, proyecto)


@router.get(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    summary="Obtener un proyecto por ID",
    description="Busca un proyecto por su ID. Devuelve 404 si no existe."
)
def obtener_proyecto(proyecto_id: int):
    proyecto = repositorio.obtener_proyecto(proyecto_id)
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con ID {proyecto_id} no encontrado."
        )
    return _a_response(proyecto_id, proyecto)


@router.post(
    "/{proyecto_id}/tareas",
    response_model=TareaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar una tarea a un proyecto",
    description="Crea una tarea y la agrega al proyecto indicado. "
                "Devuelve 404 si el proyecto no existe, 422 si el título es inválido."
)
def agregar_tarea(proyecto_id: int, body: TareaRequest):
    proyecto = repositorio.obtener_proyecto(proyecto_id)
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con ID {proyecto_id} no encontrado."
        )
    try:
        tarea = Tarea(
            titulo=body.titulo,
            descripcion=body.descripcion,
            prioridad=body.prioridad
        )
        proyecto.agregar_tarea(tarea)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    tid = repositorio.guardar_tarea(tarea)
    return _a_response_tarea(tid, tarea)


# ── Helpers ───────────────────────────────────────────────────────────────────

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
        fecha_creacion=proyecto.fecha_creacion
    )


def _a_response_tarea(tid: int, tarea: Tarea) -> TareaResponse:
    return TareaResponse(
        id=tid,
        titulo=tarea._titulo,
        descripcion=tarea.descripcion,
        estado=tarea._estado,
        prioridad=tarea._prioridad,
        fecha_creacion=tarea.fecha_creacion,
        fecha_completada=tarea._fecha_completada
    )
