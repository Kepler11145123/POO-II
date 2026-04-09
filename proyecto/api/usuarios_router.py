"""
usuarios_router.py — Endpoints para la entidad Usuario.

GET  /usuarios          → listar todos los usuarios
POST /usuarios          → crear un nuevo usuario
GET  /usuarios/{id}     → obtener un usuario por ID
"""
from fastapi import APIRouter, HTTPException, status
from proyecto.api.models  import UsuarioRequest, UsuarioResponse
from proyecto.src.domain.usuario import Usuario
from proyecto.src.infrastructure.repositories import usuario_repo as repositorio

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get(
    "/",
    response_model=list[UsuarioResponse],
    summary="Listar todos los usuarios",
    description="Devuelve la lista completa de usuarios registrados en el sistema."
)
def listar_usuarios():
    resultado = []
    for uid, usuario in repositorio.listar_usuarios():
        resultado.append(_a_response(uid, usuario))
    return resultado


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Crea un usuario con username, email y nombre completo opcional. "
                "Devuelve 422 si el username o email no son válidos."
)
def crear_usuario(body: UsuarioRequest):
    try:
        usuario = Usuario(
            username=body.username,
            email=body.email,
            nombre_completo=body.nombre_completo
        )
    except ValueError as e:
        # La clase lanza ValueError — lo convertimos en 422
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    uid = repositorio.guardar_usuario(usuario)
    return _a_response(uid, usuario)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Obtener un usuario por ID",
    description="Busca un usuario por su ID. Devuelve 404 si no existe."
)
def obtener_usuario(usuario_id: int):
    usuario = repositorio.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado."
        )
    return _a_response(usuario_id, usuario)


# ── Helper ────────────────────────────────────────────────────────────────────

def _a_response(uid: int, usuario: Usuario) -> UsuarioResponse:
    """Convierte un objeto Usuario del dominio a UsuarioResponse."""
    return UsuarioResponse(
        id=uid,
        username=usuario.username,
        email=usuario.email,
        nombre_completo=usuario._nombre_completo,
        activo=usuario._activo,
        fecha_registro=usuario.fecha_registro
    )
