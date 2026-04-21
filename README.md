# TaskFlow — Sistema de Gestión de Proyectos y Tareas

API REST construida con **FastAPI**, persistencia en **JSON**, frontend dinámico con **HTMX** y templates **Jinja2**.

---

##  Estructura del proyecto

```
proyecto/
├── api/
│   ├── main.py                  # Punto de entrada de FastAPI
│   ├── models.py                # Schemas Pydantic (Request / Response)
│   ├── dependencies.py          # Inyección de dependencias
│   ├── usuarios_router.py
│   ├── proyectos_router.py
│   ├── tareas_router.py
│   └── routes/
│       └── auth.py              # Login JWT
├── auth/
│   └── jwt_handler.py           # Creación y verificación de tokens
├── src/
│   ├── domain/
│   │   ├── enums.py             # PrioridadTarea, EstadoTarea
│   │   ├── usuario.py
│   │   ├── tarea.py
│   │   └── proyecto.py
│   ├── infrastructure/
│   │   ├── csv_database.py      # Inicialización de archivos JSON
│   │   └── repositories/
│   │       ├── interfaces.py    # ABCs: IUsuario/IProyecto/ITareaRepository
│   │       ├── usuario_repo.py
│   │       ├── proyecto_repo.py
│   │       └── tarea_repo.py
│   └── data/                    # Archivos JSON de persistencia
│       ├── usuarios.json
│       ├── proyectos.json
│       └── tareas.json
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── proyectos/
│   │   ├── lista.html
│   │   └── form.html
│   └── tareas/
│       ├── lista.html
│       └── item.html
├── static/
│   └── css/custom.css
├── tests/
│   ├── conftest.py
│   ├── test_enums.py
│   ├── test_usuario.py
│   ├── test_tarea.py
│   └── test_proyecto.py
└── pytest.ini
```

---

##  Requisitos

- Python 3.10+
- pip

---

##  Instalación

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd proyecto

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

##  Ejecución del servidor

```bash
uvicorn proyecto.api.main:app --reload
```

- API: http://127.0.0.1:8000
- Documentación Swagger: http://127.0.0.1:8000/docs
- Frontend: http://127.0.0.1:8000/

---

##  Endpoints

###  Auth

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/auth/login` | Login con `username`/`password`, retorna JWT |

###  Usuarios

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/usuarios/` | Listar todos los usuarios |
| `POST` | `/usuarios/` | Crear usuario |
| `GET` | `/usuarios/{id}` | Obtener usuario por ID |

###  Proyectos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/proyectos` | Listar proyectos (HTML vía HTMX) |
| `POST` | `/proyectos` | Crear proyecto |
| `GET` | `/proyectos/{id}/tareas` | Ver tareas de un proyecto |
| `POST` | `/proyectos/{id}/tareas` | Agregar tarea a un proyecto |
| `DELETE` | `/proyectos/{id}` | Eliminar proyecto |

###  Tareas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `PATCH` | `/tareas/{id}/completar` | Marcar como completada (HTML) |
| `PATCH` | `/tareas/{id}/prioridad` | Cambiar prioridad (HTML) |
| `PATCH` | `/tareas/{id}/completar/json` | Marcar como completada (JSON) |
| `PATCH` | `/tareas/{id}/prioridad/json` | Cambiar prioridad (JSON) |

###  Códigos de estado

| Código | Significado |
|--------|-------------|
| `200` | Operación exitosa |
| `201` | Recurso creado |
| `401` | No autenticado |
| `404` | Recurso no encontrado |
| `422` | Error de validación |

---

##  Modelos de dominio

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

```
PENDIENTE → EN_PROGRESO → COMPLETADA
PENDIENTE →              COMPLETADA   (también válido)
```

### Schemas Pydantic

- `UsuarioRequest` / `UsuarioResponse`
- `ProyectoRequest` / `ProyectoResponse`
- `TareaRequest` / `TareaResponse`
- `CambiarPrioridadRequest`

**Validaciones incluidas:** longitud mínima de username (3 chars), formato de email, longitud mínima de nombre de proyecto y título de tarea (3 chars).

---

## Frontend (HTMX + Jinja2)

El frontend no usa JavaScript personalizado. Toda la interactividad se maneja con atributos HTMX:

- `hx-get` / `hx-post` / `hx-patch` / `hx-delete`
- `hx-target` / `hx-swap` / `hx-trigger`
- `hx-confirm` para confirmaciones de eliminación

**Funcionalidades:** listado dinámico de proyectos, creación sin recarga, gestión de tareas por proyecto, completar tareas y cambiar prioridad en tiempo real.

---

##  Autenticación JWT

El módulo `proyecto/auth/jwt_handler.py` implementa la creación y verificación de tokens HS256. El endpoint `/auth/login` acepta `OAuth2PasswordRequestForm` y retorna un `access_token` de tipo Bearer.

>  **Importante:** cambiar `SECRET_KEY` en `jwt_handler.py` antes de cualquier despliegue.

---

##  Bugs conocidos

Los siguientes errores están presentes en el código fuente actual:

- **`usuario.py`** — `hashear()` tiene un typo: `password.encodne()` debería ser `password.encode()`. Esto hace que el hashing de contraseñas falle en tiempo de ejecución.
- **`usuario.py`** — El constructor asigna con `==` en lugar de `=`: `self._password_hash == hashear(password)` no asigna el hash.
- **`usuario.py`** — El método está definido como `verificar_contraseña` pero `auth.py` llama a `verificar_password` (nombre diferente).
- **`proyecto.py`** — `from_dict` referencia `data["Lider"]` (con L mayúscula) en lugar de `data["lider"]`, lo que causa `KeyError` al deserializar.
- **`repositories/__init__.py`** — `obtener_tarea` no está definido como función de módulo; `tareas_router.py` llama a `repositories.obtener_tarea(tarea_id)` que no existe en ese namespace.

---

##  Tests

Los tests usan `pytest` con fixtures definidas en `conftest.py`. Están organizados por clase y cubren creación, validaciones, cambios de estado y filtros.

```bash
# Desde la raíz del proyecto
pytest proyecto/ -v
```

**Marcadores disponibles:**

- `unit` — tests unitarios puros
- `integration` — tests de integración
- `smoke` — pruebas críticas rápidas

```bash
pytest -m unit
pytest -m smoke
```

---

##  Ejemplo de uso del dominio

```python
from proyecto.src.domain.enums import PrioridadTarea
from proyecto.src.domain.usuario import Usuario
from proyecto.src.domain.tarea import Tarea
from proyecto.src.domain.proyecto import Proyecto

# Crear entidades
usuario  = Usuario("juan123", "juan@mail.com", "Juan Pérez")
proyecto = Proyecto("Mi App", lider=usuario)

# Agregar y gestionar tareas
tarea = Tarea("Diseñar base de datos", prioridad=PrioridadTarea.ALTA)
proyecto.agregar_tarea(tarea)

tarea.iniciar()   # → EN_PROGRESO
tarea.completar() # → COMPLETADA

# Consultas
pendientes = proyecto.obtener_tareas_pendientes()
altas      = proyecto.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
```