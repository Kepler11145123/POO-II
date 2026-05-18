from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from proyecto.api.models import ProyectoRequest, ProyectoResponse, TareaResponse
from proyecto.api.dependencies import get_proyecto_repo, get_tarea_repo, get_current_user
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.tarea import Tarea
from proyecto.src.domain.enums import PrioridadTarea
from database.repositories.proyecto_repo import ProyectoRepository
from database.repositories.tarea_repo import TareaRepository

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])
templates = Jinja2Templates(directory="proyecto/templates")

# --- HTML (HTMX) ---

@router.get("", response_class=HTMLResponse, include_in_schema=False)
def listar_proyectos_html(
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    current_user = Depends(get_current_user),
):
    proyectos = [_a_response(pid, p) for pid, p in repo.listar_por_lider(current_user.id)]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

@router.post("", response_class=HTMLResponse, include_in_schema=False)
async def crear_proyecto_html(
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    current_user = Depends(get_current_user),
):
    form = await request.form()
    try:
        proyecto = Proyecto(
            nombre=form.get("nombre", ""),
            descripcion=form.get("descripcion") or None,
            lider=current_user,
        )
        repo.guardar(proyecto, lider_id=current_user.id)
    except ValueError as e:
        proyectos = [_a_response(pid, p) for pid, p in repo.listar_por_lider(current_user.id)]
        return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos, "error": str(e)})
    proyectos = [_a_response(pid, p) for pid, p in repo.listar_por_lider(current_user.id)]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

@router.get("/{proyecto_id}/tareas", response_class=HTMLResponse, include_in_schema=False)
def listar_tareas_html(
    proyecto_id: int,
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    current_user = Depends(get_current_user),
):
    proyecto = repo.obtener_para_lider(proyecto_id, current_user.id)
    if not proyecto:
        return HTMLResponse("<p>No encontrado</p>", status_code=404)
    tareas = [_a_response_tarea(t._id, t) for t in proyecto.tareas]
    return templates.TemplateResponse(request, "tareas/lista.html", {"tareas": tareas, "proyecto_id": proyecto_id})

@router.post("/{proyecto_id}/tareas", response_class=HTMLResponse, include_in_schema=False)
async def agregar_tarea_html(
    proyecto_id: int,
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    repo_t: TareaRepository = Depends(get_tarea_repo),
    current_user = Depends(get_current_user),
):
    proyecto = repo.obtener_para_lider(proyecto_id, current_user.id)
    if not proyecto:
        return HTMLResponse("<p>No encontrado</p>", status_code=404)

    form = await request.form()
    try:
        prioridad = PrioridadTarea(form.get("prioridad", PrioridadTarea.MEDIA.value))
        nueva_tarea = Tarea(
            titulo=form.get("titulo", ""),
            descripcion=form.get("descripcion") or None,
            prioridad=prioridad,
        )
        repo_t.guardar(nueva_tarea, proyecto_id)
    except ValueError as e:
        return HTMLResponse(f"<p>Error: {e}</p>", status_code=400)

    proyecto = repo.obtener_para_lider(proyecto_id, current_user.id)
    tareas = [_a_response_tarea(t._id, t) for t in proyecto.tareas]
    return templates.TemplateResponse(request, "tareas/lista.html", {"tareas": tareas, "proyecto_id": proyecto_id})

@router.delete("/{proyecto_id}", response_class=HTMLResponse, include_in_schema=False)
def eliminar_proyecto_html(
    proyecto_id: int,
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    current_user = Depends(get_current_user),
):
    try:
        repo.eliminar_para_lider(proyecto_id, current_user.id)
    except Exception as e:
        proyectos = [_a_response(pid, p) for pid, p in repo.listar_por_lider(current_user.id)]
        return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos, "error": str(e)})
    proyectos = [_a_response(pid, p) for pid, p in repo.listar_por_lider(current_user.id)]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

# --- JSON ---

@router.get("/json", response_model=list[ProyectoResponse])
def listar_proyectos_json(repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    return [_a_response(pid, p) for pid, p in repo.listar_por_lider(current_user.id)]

@router.post("/json", response_model=ProyectoResponse, status_code=201)
def crear_proyecto_json(body: ProyectoRequest, repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    try:
        proyecto = Proyecto(nombre=body.nombre, descripcion=body.descripcion, lider=current_user)
        pid, _ = repo.guardar(proyecto, lider_id=current_user.id)
        return _a_response(pid, proyecto)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/json/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto_json(proyecto_id: int, body: ProyectoRequest, repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    proyecto = repo.obtener_para_lider(proyecto_id, current_user.id)
    if not proyecto:
        raise HTTPException(status_code=404, detail=f"Proyecto {proyecto_id} no encontrado.")
    proyecto = Proyecto(nombre=body.nombre, descripcion=body.descripcion, lider=current_user)
    repo.actualizar(proyecto_id, proyecto)
    actualizado = repo.obtener_para_lider(proyecto_id, current_user.id)
    return _a_response(proyecto_id, actualizado)

@router.delete("/json/{proyecto_id}", status_code=204)
def eliminar_proyecto_json(proyecto_id: int, repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    if not repo.eliminar_para_lider(proyecto_id, current_user.id):
        raise HTTPException(status_code=404, detail=f"Proyecto {proyecto_id} no encontrado.")

# --- Helpers ---

def _a_response(pid: int, proyecto: Proyecto) -> ProyectoResponse:
    return ProyectoResponse(
        id=pid,
        nombre=proyecto.nombre,
        lider_id=getattr(proyecto.lider, "id", None) if proyecto.lider else None,
        total_tareas=len(proyecto.tareas),
        fecha_creacion=proyecto.fecha_creacion
    )

def _a_response_tarea(tid: int, tarea: Tarea) -> TareaResponse:
    return TareaResponse(
        id=tid,
        titulo=tarea._titulo,
        descripcion=tarea.descripcion,
        estado=tarea._estado.value if hasattr(tarea._estado, 'value') else tarea._estado,
        prioridad=tarea._prioridad.value if hasattr(tarea._prioridad, 'value') else tarea._prioridad,
        fecha_creacion=tarea.fecha_creacion,
        fecha_completada=tarea._fecha_completada
    )
