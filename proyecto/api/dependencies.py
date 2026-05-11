from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database.connection import get_db
from database.repositories.usuario_repo import UsuarioRepository
from database.repositories.proyecto_repo import ProyectoRepository
from database.repositories.tarea_repo import TareaRepository
from proyecto.auth.jwt_handler import verificar_token

def get_usuario_repo(db: Session = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepository(db)

def get_proyecto_repo(db: Session = Depends(get_db)) -> ProyectoRepository:
    return ProyectoRepository(db)

def get_tarea_repo(db: Session = Depends(get_db)) -> TareaRepository:
    return TareaRepository(db)

def get_current_user(request: Request, repo: UsuarioRepository = Depends(get_usuario_repo)):
    token = request.cookies.get("access_token") or request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    if not token:
        raise HTTPException(status_code=401, detail="No autorizado")
    try:
        payload = verificar_token(token)
        username = payload.get("sub")
        user_id = payload.get("id")
        resultado = repo.obtener_por_username(username)
        if not resultado or resultado[0] != user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        return resultado[1]
    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido")