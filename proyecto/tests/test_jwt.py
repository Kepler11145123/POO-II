import asyncio
from datetime import timedelta
from http.cookies import SimpleCookie

import pytest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import models  # noqa: F401
from database.base import Base
from database.repositories.usuario_repo import UsuarioRepository
from proyecto.api.auth_router import login, register, registrar_usuario
from proyecto.auth.jwt_handler import crear_token, decode_token, verificar_token
from proyecto.src.domain.usuario import Usuario


def test_crear_y_verificar_token_jwt():
    token = crear_token("juan123", 42)

    payload = verificar_token(token)

    assert payload["sub"] == "juan123"
    assert payload["id"] == 42
    assert "exp" in payload


def test_decode_token_mantiene_compatibilidad():
    token = crear_token("maria99", 7)

    payload = decode_token(token)

    assert payload["sub"] == "maria99"
    assert payload["id"] == 7


def test_token_invalido_lanza_value_error():
    with pytest.raises(ValueError, match="Token invalido"):
        verificar_token("token.invalido")


def test_token_expirado_lanza_value_error():
    token = crear_token("juan123", 42, expires_delta=timedelta(seconds=-1))

    with pytest.raises(ValueError, match="Token invalido"):
        verificar_token(token)


def test_login_emite_cookie_jwt_valida():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        repo = UsuarioRepository(db)
        repo.guardar(
            Usuario(
                username="loginuser",
                email="login@example.com",
                password="secreto123",
            )
        )
    finally:
        db.close()

    db = TestingSessionLocal()
    try:
        repo = UsuarioRepository(db)
        form = OAuth2PasswordRequestForm(
            username="loginuser",
            password="secreto123",
        )
        response = asyncio.run(login(None, form=form, repo=repo))
    finally:
        db.close()

    assert response.status_code == 302
    cookies = SimpleCookie()
    cookies.load(response.headers["set-cookie"])
    token = cookies["access_token"].value

    payload = verificar_token(token)
    assert payload["sub"] == "loginuser"
    assert payload["id"] == 1


def test_registrar_usuario_guarda_password_hash():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        repo = UsuarioRepository(db)
        uid, usuario = registrar_usuario(
            repo=repo,
            username="nuevo123",
            email="nuevo@example.com",
            nombre_completo="Nuevo Usuario",
            password="secreto123",
            confirmar_password="secreto123",
        )

        guardado = repo.obtener_por_username("nuevo123")
    finally:
        db.close()

    assert uid == 1
    assert usuario.verificar_password("secreto123")
    assert guardado is not None
    assert guardado[1].verificar_password("secreto123")


def test_registrar_usuario_rechaza_username_duplicado():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        repo = UsuarioRepository(db)
        registrar_usuario(
            repo=repo,
            username="duplicado",
            email="uno@example.com",
            nombre_completo=None,
            password="secreto123",
            confirmar_password="secreto123",
        )

        with pytest.raises(ValueError, match="usuario ya existe"):
            registrar_usuario(
                repo=repo,
                username="duplicado",
                email="dos@example.com",
                nombre_completo=None,
                password="secreto123",
                confirmar_password="secreto123",
            )
    finally:
        db.close()


def test_register_emite_cookie_jwt_valida():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        repo = UsuarioRepository(db)
        response = asyncio.run(
            register(
                None,
                username="webuser",
                email="webuser@example.com",
                nombre_completo="Web User",
                password="secreto123",
                confirmar_password="secreto123",
                repo=repo,
            )
        )
    finally:
        db.close()

    assert response.status_code == 302
    cookies = SimpleCookie()
    cookies.load(response.headers["set-cookie"])
    token = cookies["access_token"].value

    payload = verificar_token(token)
    assert payload["sub"] == "webuser"
    assert payload["id"] == 1
