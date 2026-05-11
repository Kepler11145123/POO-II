from fastapi import APIRouter, HTTPException, status, Depends
from proyecto.api.models import UsuarioRequest, UsuarioResponse
from proyecto.src.domain.usuario import Usuario
from proyecto.api.dependencies import get_usuario_repo, get_current_user
from database.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(repo: UsuarioRepository = Depends(get_usuario_repo), current_user = Depends(get_current_user)):
    return [_a_response(uid, u) for uid, u in repo.listar()]

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(body: UsuarioRequest, repo: UsuarioRepository = Depends(get_usuario_repo), current_user = Depends(get_current_user)):
    try:
        usuario = Usuario(username=body.username, email=body.email, nombre_completo=body.nombre_completo)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    uid, _ = repo.guardar(usuario)
    return _a_response(uid, usuario)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, repo: UsuarioRepository = Depends(get_usuario_repo), current_user = Depends(get_current_user)):
    usuario = repo.obtener(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario {usuario_id} no encontrado.")
    return _a_response(usuario_id, usuario)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, body: UsuarioRequest, repo: UsuarioRepository = Depends(get_usuario_repo), current_user = Depends(get_current_user)):
    usuario = repo.obtener(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario {usuario_id} no encontrado.")
    usuario.email           = body.email
    usuario._nombre_completo = body.nombre_completo
    resultado = repo.actualizar(usuario_id, usuario)
    return _a_response(resultado[0], usuario)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, repo: UsuarioRepository = Depends(get_usuario_repo), current_user = Depends(get_current_user)):
    eliminado = repo.eliminar(usuario_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail=f"Usuario {usuario_id} no encontrado.")

def _a_response(uid: int, usuario: Usuario) -> UsuarioResponse:
    return UsuarioResponse(
        id=uid,
        username=usuario.username,
        email=usuario.email,
        nombre_completo=usuario._nombre_completo,
        activo=usuario._activo,
        fecha_registro=usuario.fecha_registro
    )