from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from proyecto.api.models import ProyectoRequest, ProyectoResponse, TareaResponse
from proyecto.api.dependencies import get_proyecto_repo, get_usuario_repo, get_tarea_repo, get_current_user
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.tarea import Tarea
from proyecto.src.domain.enums import PrioridadTarea
from database.repositories.proyecto_repo import ProyectoRepository
from database.repositories.usuario_repo import UsuarioRepository
from database.repositories.tarea_repo import TareaRepository
from proyecto.auth.jwt_handler import verificar_token
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/proyectos", tags=["Proyectos"])
templates = Jinja2Templates(directory="proyecto/templates")

# --- HTML (HTMX) ---

@router.get("", response_class=HTMLResponse, include_in_schema=False)
def listar_proyectos_html(request: Request, repo: ProyectoRepository = Depends(get_proyecto_repo)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login")
    try:
        verificar_token(token)
    except ValueError:
        return RedirectResponse("/auth/login")
    proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

@router.post("", response_class=HTMLResponse, include_in_schema=False)
async def crear_proyecto_html(
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    u_repo: UsuarioRepository = Depends(get_usuario_repo)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login")
    try:
        verificar_token(token)
    except ValueError:
        return RedirectResponse("/auth/login")
    form = await request.form()
    lider_id = form.get("lider_id")
    lider = u_repo.obtener(int(lider_id)) if lider_id else None
    try:
        proyecto = Proyecto(nombre=form.get("nombre", ""), lider=lider)
        repo.guardar(proyecto)
    except ValueError as e:
        proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
        return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos, "error": str(e)})
    proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

@router.get("/{proyecto_id}/tareas", response_class=HTMLResponse, include_in_schema=False)
def listar_tareas_html(proyecto_id: int, request: Request, repo: ProyectoRepository = Depends(get_proyecto_repo)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login")
    try:
        verificar_token(token)
    except ValueError:
        return RedirectResponse("/auth/login")
    proyecto = repo.obtener(proyecto_id)
    if not proyecto:
        return HTMLResponse("<p>No encontrado</p>", status_code=404)
    tareas = [_a_response_tarea(t._id, t) for t in proyecto.tareas]
    return templates.TemplateResponse(request, "tareas/lista.html", {"tareas": tareas, "proyecto_id": proyecto_id})

@router.post("/{proyecto_id}/tareas", response_class=HTMLResponse, include_in_schema=False)
async def agregar_tarea_html(
    proyecto_id: int,
    request: Request,
    repo: ProyectoRepository = Depends(get_proyecto_repo),
    repo_t: TareaRepository = Depends(get_tarea_repo)
):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login")
    try:
        verificar_token(token)
    except ValueError:
        return RedirectResponse("/auth/login")
    proyecto = repo.obtener(proyecto_id)
    form = await request.form()
    try:
        nueva_tarea = Tarea(titulo=form.get("titulo", ""), prioridad=PrioridadTarea.ALTA)
        repo_t.guardar(nueva_tarea, proyecto_id)
        proyecto.agregar_tarea(nueva_tarea)
        repo.actualizar(proyecto_id, proyecto)
    except ValueError as e:
        return HTMLResponse(f"<p>Error: {e}</p>", status_code=400)
    tareas = [_a_response_tarea(idx, t) for idx, t in enumerate(proyecto.tareas)]
    return templates.TemplateResponse(request, "tareas/lista.html", {"tareas": tareas, "proyecto_id": proyecto_id})

@router.delete("/{proyecto_id}", response_class=HTMLResponse, include_in_schema=False)
def eliminar_proyecto_html(proyecto_id: int, request: Request, repo: ProyectoRepository = Depends(get_proyecto_repo)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/auth/login")
    try:
        verificar_token(token)
    except ValueError:
        return RedirectResponse("/auth/login")
    try:
        repo.eliminar(proyecto_id)
    except Exception as e:
        proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
        return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos, "error": str(e)})
    proyectos = [_a_response(pid, p) for pid, p in repo.listar()]
    return templates.TemplateResponse(request, "proyectos/lista.html", {"proyectos": proyectos})

# --- JSON ---

@router.get("/json", response_model=list[ProyectoResponse])
def listar_proyectos_json(repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    return [_a_response(pid, p) for pid, p in repo.listar()]

@router.post("/json", response_model=ProyectoResponse, status_code=201)
def crear_proyecto_json(body: ProyectoRequest, repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    try:
        proyecto = Proyecto(nombre=body.nombre)
        pid, _ = repo.guardar(proyecto)
        return _a_response(pid, proyecto)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/json/{proyecto_id}", response_model=ProyectoResponse)
def actualizar_proyecto_json(proyecto_id: int, body: ProyectoRequest, repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    proyecto = repo.obtener(proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail=f"Proyecto {proyecto_id} no encontrado.")
    proyecto.nombre = body.nombre
    repo.actualizar(proyecto_id, proyecto)
    return _a_response(proyecto_id, proyecto)

@router.delete("/json/{proyecto_id}", status_code=204)
def eliminar_proyecto_json(proyecto_id: int, repo: ProyectoRepository = Depends(get_proyecto_repo), current_user = Depends(get_current_user)):
    if not repo.eliminar(proyecto_id):
        raise HTTPException(status_code=404, detail=f"Proyecto {proyecto_id} no encontrado.")

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
        prioridad=tarea._prioridad.value if hasattr(tarea._prioridad, 'value') else tarea._prioridad,
        fecha_creacion=tarea.fecha_creacion,
        fecha_completada=tarea._fecha_completada
    )