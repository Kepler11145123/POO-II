from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import models  # noqa: F401
from database.base import Base
from database.repositories.proyecto_repo import ProyectoRepository
from database.repositories.tarea_repo import TareaRepository
from database.repositories.usuario_repo import UsuarioRepository
from proyecto.src.domain.enums import PrioridadTarea
from proyecto.src.domain.proyecto import Proyecto
from proyecto.src.domain.tarea import Tarea
from proyecto.src.domain.usuario import Usuario


def crear_repositorios():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    return db, UsuarioRepository(db), ProyectoRepository(db), TareaRepository(db)


def test_proyectos_y_tareas_se_filtran_por_usuario():
    db, usuarios, proyectos, tareas = crear_repositorios()
    try:
        user_a_id, user_a = usuarios.guardar(
            Usuario("usuarioa", "a@example.com", password="secreto123")
        )
        user_b_id, user_b = usuarios.guardar(
            Usuario("usuariob", "b@example.com", password="secreto123")
        )

        proyecto_a_id, _ = proyectos.guardar(
            Proyecto("Proyecto A", lider=user_a),
            lider_id=user_a_id,
        )
        proyecto_b_id, _ = proyectos.guardar(
            Proyecto("Proyecto B", lider=user_b),
            lider_id=user_b_id,
        )

        tarea_a_id, _ = tareas.guardar(
            Tarea("Tarea A", prioridad=PrioridadTarea.ALTA),
            proyecto_a_id,
        )
        tarea_b_id, _ = tareas.guardar(
            Tarea("Tarea B", prioridad=PrioridadTarea.MEDIA),
            proyecto_b_id,
        )

        proyectos_a = proyectos.listar_por_lider(user_a_id)
        tareas_a = tareas.listar_por_lider(user_a_id)

        assert [pid for pid, _ in proyectos_a] == [proyecto_a_id]
        assert [tid for tid, _ in tareas_a] == [tarea_a_id]
        assert proyectos.obtener_para_lider(proyecto_b_id, user_a_id) is None
        assert tareas.obtener_para_lider(tarea_b_id, user_a_id) is None
    finally:
        db.close()
