# TaskFlow - Sistema de Gestión de Tareas

Proyecto de modelado orientado a objetos con las entidades principales de un sistema de gestión de tareas.

## Estructura del proyecto
```
src/
└── domain/
    ├── enums.py
    ├── usuario.py
    ├── tarea.py
    └── proyecto.py
test_dominio.py
```

## Requisitos

- Python 3.10+
- pytest
```bash
pip install pytest
```

## Correr los tests

Desde la carpeta raíz del proyecto (`POO II`):
```bash
python -m pytest test_dominio.py -v
```

## Ejemplos de uso
```python
from src.domain.enums import PrioridadTarea, EstadoTarea
from src.domain.usuario import Usuario
from src.domain.tarea import Tarea
from src.domain.proyecto import Proyecto

# Crear un usuario
usuario = Usuario("juan123", "juan@mail.com", "Juan Pérez")

# Crear un proyecto
proyecto = Proyecto("Mi App", lider=usuario)

# Crear y agregar tareas
tarea = Tarea("Diseñar base de datos", prioridad=PrioridadTarea.ALTA)
proyecto.agregar_tarea(tarea)

# Cambiar estado de una tarea
tarea.iniciar()   # EN_PROGRESO
tarea.completar() # COMPLETADA

# Consultar tareas
pendientes = proyecto.obtener_tareas_pendientes()
altas      = proyecto.obtener_tareas_por_prioridad(PrioridadTarea.ALTA)
```

# 📌 Proyecto POO-II - API de Gestión de Proyectos y Tareas

Este proyecto implementa una API REST utilizando **FastAPI**, junto con un frontend dinámico basado en **HTMX** y templates con **Jinja2**.

---

## 🚀 Requisitos

* Python 3.10+
* pip (gestor de paquetes)

---

## 📦 Instalación

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto
```

2. Crear entorno virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución del servidor

Para iniciar la aplicación con **Uvicorn**:

```bash
uvicorn src.main:app --reload
```

> ⚠️ Asegúrate de que el archivo principal esté en `src/main.py` y contenga la instancia `app = FastAPI()`.

---

## 🌐 Acceso a la aplicación

* API: http://127.0.0.1:8000
* Documentación Swagger: http://127.0.0.1:8000/docs

---

## 📡 Endpoints disponibles

### 👤 Usuarios

* `GET /usuarios` → Listar usuarios
* `POST /usuarios` → Crear usuario
* `GET /usuarios/{id}` → Obtener usuario por ID

### 📁 Proyectos

* `GET /proyectos` → Listar proyectos
* `POST /proyectos` → Crear proyecto
* `GET /proyectos/{id}` → Obtener proyecto
* `POST /proyectos/{id}/tareas` → Crear tarea en proyecto

### ✅ Tareas

* `PATCH /tareas/{id}/completar` → Marcar como completada
* `PATCH /tareas/{id}/prioridad` → Cambiar prioridad

---

## 📊 Códigos de estado

* `200 OK` → Operación exitosa
* `201 Created` → Recurso creado
* `404 Not Found` → Recurso no encontrado
* `422 Unprocessable Entity` → Error de validación

---

## 🧠 Modelos Pydantic

Se utilizan modelos para validación y serialización:

* `UsuarioCreate`
* `UsuarioResponse`
* `ProyectoCreate`
* `TareaCreate`
* `TareaUpdate`

Validaciones incluyen:

* `Field(min_length=3, max_length=50)`
* `EmailStr` para emails
* Valores por defecto para prioridad

---

## 🖥️ Frontend (HTMX + Jinja2)

### Funcionalidades

* Listado de proyectos dinámico
* Creación de proyectos sin recargar página
* Listado de tareas por proyecto
* Completar tareas dinámicamente
* Cambio de prioridad en tiempo real

### Atributos HTMX usados

* `hx-get`
* `hx-post`
* `hx-patch`
* `hx-target`
* `hx-swap`
* `hx-trigger`

> ❗ No se utiliza JavaScript personalizado.

---

## 📁 Estructura del proyecto

```
proyecto/
│
├── api/
├── features/
├── src/
├── static/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── proyectos/
│   │   ├── lista.html
│   │   └── form.html
│   └── tareas/
│       ├── lista.html
│       └── item.html
│
├── tests/
├── requirements.txt
├── README.md
└── pytest.ini
```

---

## 🧪 Tests

Para ejecutar los tests:

```bash
pytest
```

---

## 📌 Notas

* Toda la renderización HTML se realiza con **Jinja2**
* La interactividad se maneja exclusivamente con **HTMX**
* La API cuenta con documentación automática en `/docs`

---


