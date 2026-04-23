from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from proyecto.api.models import ProyectoRequest, ProyectoResponse, TareaResponse
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.tarea import Tarea
from proyecto.src.domain.enums import PrioridadTarea

# Inyección de dependencias necesaria para la rúbrica
from proyecto.api.dependencies import get_proyecto_repo, get_usuario_repo, get_tarea_repo
from proyecto.src.infrastructure.repositories.interfaces import (
    IProyectoRepository, IUsuarioRepository, ITareaRepository
)

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])
templates = Jinja2Templates(directory="proyecto/templates")

# --- Endpoints HTML (HTMX) ---

@router.get("", response_class=HTMLResponse, include_in_schema=False)
def listar_proyectos_html(
    request: Request, 
    repo: IProyectoRepository = Depends(get_proyecto_repo)
):
    proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

@router.post("", response_class=HTMLResponse, include_in_schema=False)
async def crear_proyecto_html(
    request: Request, 
    repo: IProyectoRepository = Depends(get_proyecto_repo),
    u_repo: IUsuarioRepository = Depends(get_usuario_repo)
):
    form = await request.form()
    lider_id = form.get("lider_id")
    lider = u_repo.obtener(int(lider_id)) if lider_id else None

    try:
        proyecto = Proyecto(nombre=form.get("nombre", ""), lider=lider)
        repo.guardar(proyecto) # Usa 'guardar' como definiste en tu clase
    except ValueError as e:
        proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
        return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos, "error": str(e)})

    proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

@router.get("/{proyecto_id}/tareas", response_class=HTMLResponse, include_in_schema=False)
def listar_tareas_html(
    proyecto_id: int, 
    request: Request, 
    repo_p: IProyectoRepository = Depends(get_proyecto_repo)
):
    proyecto = repo_p.obtener(proyecto_id)
    if not proyecto:
        return HTMLResponse("<p>No encontrado</p>", status_code=404)
    
    # Aquí el dominio ya tiene sus tareas cargadas
    tareas = [_a_response_tarea(idx, t) for idx, t in enumerate(proyecto.tareas)]
    return templates.TemplateResponse(request, "tareas/lista.html", {"tareas": tareas, "proyecto_id": proyecto_id})

@router.post("/{proyecto_id}/tareas", response_class=HTMLResponse, include_in_schema=False)
async def agregar_tarea_html(
    proyecto_id: int, 
    request: Request,
    repo_p: IProyectoRepository = Depends(get_proyecto_repo),
    repo_t: ITareaRepository = Depends(get_tarea_repo)
):
    proyecto = repo_p.obtener(proyecto_id)
    form = await request.form()
    
    try:
        nueva_tarea = Tarea(titulo=form.get("titulo", ""), prioridad=PrioridadTarea.ALTA)
        repo_t.guardar(nueva_tarea, proyecto_id)  # se pasa el proyecto_id
        proyecto.agregar_tarea(nueva_tarea)
        repo_p.guardar(proyecto)
    except ValueError as e:
        return HTMLResponse(f"<p>Error: {e}</p>", status_code=400)

    tareas = [_a_response_tarea(idx, t) for idx, t in enumerate(proyecto.tareas)]
    return templates.TemplateResponse(request, "tareas/lista.html", {"tareas": tareas, "proyecto_id": proyecto_id})

@router.delete("/{proyecto_id}", response_class=HTMLResponse, include_in_schema=False)
def eliminar_proyecto_html(
    proyecto_id: int,
    request: Request,
    repo: IProyectoRepository = Depends(get_proyecto_repo)
):
    try:
        repo.eliminar(proyecto_id)
    except Exception as e:
        proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
        return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos, "error": f"No se pudo eliminar: {str(e)}"})
    
    proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

# --- Helpers ---

def _a_response(pid: int, proyecto: Proyecto) -> ProyectoResponse:
    return ProyectoResponse(
        id=pid,
        nombre=proyecto.nombre,
        lider_id=proyecto.lider.id if proyecto.lider else None,
        total_tareas=len(proyecto.tareas),
        fecha_creacion=proyecto.fecha_creacion
    )

def _a_response_tarea(tid: int, tarea: Tarea) -> TareaResponse:
    return TareaResponse(
        id=tid, 
        titulo=tarea._titulo, 
        descripcion=tarea.descripcion, 
        estado=tarea._estado.value if hasattr(tarea._estado, 'value') else tarea._estado,
        prioridad=tarea._prioridad.value if tarea._prioridad else None,
        fecha_creacion=tarea.fecha_creacion,
        # CORRECCIÓN: Agregamos el campo que falta
        fecha_completada=tarea._fecha_completada 
    )