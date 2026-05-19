# TaskFlow — Sistema de Gestión de Proyectos y Tareas

API REST construida con **FastAPI**, persistencia en **SQLite** via **SQLAlchemy ORM**,
migraciones con **Alembic**, autenticación **JWT**, frontend dinámico con **HTMX**
y templates **Jinja2**.

---

## Estructura del proyecto
taskflow/
├── alembic/
│   ├── env.py                        # Configuración de migraciones
│   ├── script.py.mako                # Template de revisiones
│   └── versions/
│       └── 20260514_0001_create_initial_tables.py
├── database/
│   ├── base.py                       # DeclarativeBase de SQLAlchemy
│   ├── connection.py                 # Engine, SessionLocal, get_db()
│   ├── models.py                     # Modelos ORM: Usuario, Proyecto, Tarea
│   └── repositories/
│       ├── usuario_repo.py
│       ├── proyecto_repo.py
│       └── tarea_repo.py
├── proyecto/
│   ├── api/
│   │   ├── main.py                   # Punto de entrada FastAPI
│   │   ├── models.py                 # Schemas Pydantic (Request / Response)
│   │   ├── dependencies.py           # Inyección de dependencias (DI)
│   │   ├── auth_router.py            # Login, registro, logout
│   │   ├── usuarios_router.py
│   │   ├── proyectos_router.py
│   │   └── tareas_router.py
│   ├── auth/
│   │   └── jwt_handler.py            # Creación y verificación de tokens JWT
│   ├── src/
│   │   └── domain/
│   │       ├── enums.py              # PrioridadTarea, EstadoTarea
│   │       ├── usuario.py
│   │       ├── tarea.py
│   │       └── proyecto.py
│   ├── static/
│   │   └── css/custom.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── proyectos/
│       │   ├── lista.html
│       │   └── form.html
│       └── tareas/
│           ├── lista.html
│           └── item.html
├── tests/
│   ├── conftest.py
│   ├── test_enums.py
│   ├── test_usuario.py
│   ├── test_tarea.py
│   ├── test_proyecto.py
│   ├── test_jwt.py
│   └── test_data_isolation.py
├── alembic.ini
├── create_tables.py                  # Aplica migraciones programáticamente
├── .env.example
└── pytest.ini

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Framework web | FastAPI |
| ORM | SQLAlchemy |
| Migraciones | Alembic |
| Base de datos | SQLite (por defecto) |
| Autenticación | JWT (python-jose) |
| Validación | Pydantic v2 |
| Frontend | HTMX + Jinja2 + Bootstrap 5 |
| Tests | pytest |

---

## Requisitos

- Python 3.10+
- pip

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd taskflow

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y cambiar JWT_SECRET por un valor seguro
```

---

## Base de datos y migraciones

El proyecto usa **Alembic** para gestionar el esquema de la base de datos.

```bash
# Aplicar todas las migraciones (crea las tablas)
python create_tables.py

# O directamente con Alembic
alembic upgrade head

# Ver el estado actual de las migraciones
alembic current

# Revertir la última migración
alembic downgrade -1

# Crear una nueva migración
alembic revision --autogenerate -m "descripcion del cambio"
```

La URL de la base de datos se lee desde la variable de entorno `DATABASE_URL`.
Por defecto usa SQLite: `sqlite:///./taskflow.db`.

---

## Ejecución del servidor

```bash
uvicorn proyecto.api.main:app --reload
```

- App: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Autenticación

El sistema usa **JWT (JSON Web Tokens)** con algoritmo HS256.

El flujo es:
1. El usuario se registra en `/auth/register` o inicia sesión en `/auth/login`.
2. El servidor genera un token JWT y lo guarda en una cookie `httponly`.
3. Cada request posterior envía la cookie automáticamente.
4. El módulo `dependencies.py` verifica el token en cada endpoint protegido.

> **Importante:** cambiar el valor de `JWT_SECRET` en el archivo `.env` antes de cualquier despliegue en producción. Nunca usar el valor por defecto.

---

## Endpoints

### Auth

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/auth/login` | Página de login (HTML) |
| `POST` | `/auth/login` | Autenticar usuario, retorna cookie JWT |
| `GET` | `/auth/register` | Página de registro (HTML) |
| `POST` | `/auth/register` | Crear cuenta nueva |
| `POST` | `/auth/logout` | Cerrar sesión, elimina la cookie |

### Usuarios

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/usuarios/` | Listar todos los usuarios |
| `POST` | `/usuarios/` | Crear usuario |
| `GET` | `/usuarios/{id}` | Obtener usuario por ID |
| `PUT` | `/usuarios/{id}` | Actualizar usuario |
| `DELETE` | `/usuarios/{id}` | Eliminar usuario |

### Proyectos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/proyectos` | Listar proyectos del usuario (HTML) |
| `POST` | `/proyectos` | Crear proyecto (HTML) |
| `GET` | `/proyectos/{id}/tareas` | Ver tareas del proyecto (HTML) |
| `POST` | `/proyectos/{id}/tareas` | Agregar tarea al proyecto (HTML) |
| `DELETE` | `/proyectos/{id}` | Eliminar proyecto (HTML) |
| `GET` | `/proyectos/json` | Listar proyectos (JSON) |
| `POST` | `/proyectos/json` | Crear proyecto (JSON) |
| `PUT` | `/proyectos/json/{id}` | Actualizar proyecto (JSON) |
| `DELETE` | `/proyectos/json/{id}` | Eliminar proyecto (JSON) |

### Tareas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PATCH` | `/tareas/{id}/completar` | Completar / reabrir tarea (HTML) |
| `PATCH` | `/tareas/{id}/prioridad` | Cambiar prioridad (HTML) |
| `PATCH` | `/tareas/{id}/completar/json` | Completar tarea (JSON) |
| `PATCH` | `/tareas/{id}/prioridad/json` | Cambiar prioridad (JSON) |
| `GET` | `/tareas/json` | Listar tareas del usuario (JSON) |
| `GET` | `/tareas/json/{id}` | Obtener tarea por ID (JSON) |
| `DELETE` | `/tareas/json/{id}` | Eliminar tarea (JSON) |

### Códigos de estado

| Código | Significado |
|--------|-------------|
| `200` | Operación exitosa |
| `201` | Recurso creado |
| `302` | Redirección (login/logout) |
| `401` | No autenticado |
| `404` | Recurso no encontrado |
| `422` | Error de validación |

---

## Arquitectura por capas
HTTP Request
↓
FastAPI Router          (proyecto/api/*_router.py)
↓
Dependencies / DI       (proyecto/api/dependencies.py)
↓
Repository              (database/repositories/)
↓
SQLAlchemy ORM          (database/models.py)
↓
SQLite / PostgreSQL

Cada capa tiene una responsabilidad única:

- **Routers** — reciben el request, llaman al repositorio, retornan la respuesta.
- **Dependencies** — crean la sesión de BD, instancian los repositorios, verifican el JWT.
- **Repositorios** — contienen toda la lógica de acceso a datos. Traducen entre ORM y dominio.
- **ORM** — define el esquema de la base de datos con SQLAlchemy.
- **Dominio** — clases de negocio puras sin dependencia de frameworks.

---

## Modelos de dominio

### Enums

```python
class PrioridadTarea(Enum):
    BAJA  = "Baja"
    MEDIA = "Media"
    ALTA  = "Alta"

class EstadoTarea(Enum):
    PENDIENTE   = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA  = "Completada"
```

### Ciclo de vida de una Tarea
PENDIENTE → EN_PROGRESO → COMPLETADA
PENDIENTE →              COMPLETADA   (también válido)
COMPLETADA → PENDIENTE               (toggle_completada)

### Schemas Pydantic

| Schema | Uso |
|--------|-----|
| `UsuarioRequest` | Crear usuario (valida username y email) |
| `UsuarioResponse` | Respuesta con datos del usuario |
| `ProyectoRequest` | Crear / actualizar proyecto |
| `ProyectoResponse` | Respuesta con datos del proyecto |
| `TareaRequest` | Crear tarea (valida título y prioridad) |
| `TareaResponse` | Respuesta con datos de la tarea |
| `CambiarPrioridadRequest` | Body para cambiar prioridad |

---

## Frontend (HTMX + Jinja2)

El frontend no usa JavaScript personalizado. Toda la interactividad se maneja con atributos HTMX:

- `hx-get` / `hx-post` / `hx-patch` / `hx-delete` — llamadas al servidor
- `hx-target` / `hx-swap` — dónde y cómo actualizar el DOM
- `hx-trigger` — qué evento dispara la llamada
- `hx-confirm` — confirmación antes de eliminar

**Funcionalidades:**
- Registro e inicio de sesión con redirección automática
- Listado dinámico de proyectos del usuario autenticado
- Creación de proyectos sin recargar la página
- Gestión de tareas por proyecto
- Completar / reabrir tareas en tiempo real
- Cambio de prioridad con selector inline
- Cierre de sesión con eliminación de cookie

---

## Tests

Los tests usan `pytest` con fixtures definidas en `conftest.py`.

```bash
# Ejecutar todos los tests
pytest proyecto/ -v

# Solo tests unitarios
pytest -m unit

# Solo pruebas rápidas críticas
pytest -m smoke

# Solo tests de integración
pytest -m integration
```

### Cobertura de tests

| Archivo | Qué prueba |
|---------|-----------|
| `test_enums.py` | Valores y validaciones de PrioridadTarea y EstadoTarea |
| `test_usuario.py` | Creación, validaciones, activar/desactivar |
| `test_tarea.py` | Creación, cambios de estado, prioridad |
| `test_proyecto.py` | Creación, agregar tareas, filtros |
| `test_jwt.py` | Creación/verificación de tokens, login, registro |
| `test_data_isolation.py` | Aislamiento de datos entre usuarios |

### Marcadores disponibles

| Marcador | Descripción |
|----------|-------------|
| `unit` | Tests unitarios puros |
| `integration` | Tests de integración con base de datos |
| `smoke` | Pruebas críticas rápidas |

---

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///./taskflow.db` |
| `JWT_SECRET` | Clave secreta para firmar tokens | `dev-secret-key-change-me` |
| `JWT_EXPIRE_MINUTES` | Duración del token en minutos | `60` |

---

## Ejemplo de uso del dominio

```python
from proyecto.src.domain.enums import PrioridadTarea
from proyecto.src.domain.usuario import Usuario
from proyecto.src.domain.tarea import Tarea
from proyecto.src.domain.proyecto import Proyecto

# Crear entidades
usuario  = Usuario("juan123", "juan@mail.com", "Juan Pérez", password="secreto123")
proyecto = Proyecto("Mi App", lider=usuario)

# Agregar y gestionar tareas
tarea = Tarea("Diseñar base de datos", prioridad=PrioridadTarea.ALTA)
proyecto.agregar_tarea(tarea)

tarea.iniciar()          # PENDIENTE → EN_PROGRESO
tarea.completar()        # EN_PROGRESO → COMPLETADA
tarea.toggle_completada() # COMPLETADA → PENDIENTE

# Consultas
pendientes = proyecto.obtener_tareas_pendientes()
altas      = proyecto.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)

# Verificar contraseña
usuario.verificar_password("secreto123")  # True
```