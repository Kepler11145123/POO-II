Feature: Gestión de Proyectos
  Como líder de equipo
  Quiero crear y administrar proyectos
  Para organizar el trabajo del equipo

  Background:
    Given que el sistema está inicializado
    And que existe un usuario con username "lider01" y email "lider@mail.com"

  # ── Happy Path ───────────────────────────────────────────────────────────────

  Scenario: Crear un proyecto con nombre y líder válidos
    When creo un proyecto llamado "Plataforma Web" con el líder "lider01"
    Then el proyecto "Plataforma Web" debe existir
    And el proyecto debe tener 0 tareas

  Scenario: Agregar una tarea a un proyecto
    Given que existe el proyecto "App Móvil" con el líder "lider01"
    When agrego la tarea "Diseñar pantallas" con prioridad "ALTA" al proyecto "App Móvil"
    Then el proyecto "App Móvil" debe tener 1 tarea

  Scenario: Obtener las tareas pendientes de un proyecto
    Given que existe el proyecto "Backend API" con el líder "lider01"
    And el proyecto "Backend API" tiene una tarea "Crear endpoints" con prioridad "MEDIA"
    And el proyecto "Backend API" tiene una tarea completada "Documentar DB"
    When consulto las tareas pendientes del proyecto "Backend API"
    Then debo obtener 1 tarea pendiente

  # ── Escenario de error ───────────────────────────────────────────────────────

  Scenario Outline: Crear proyecto con nombre inválido lanza error
    When intento crear un proyecto con nombre "<nombre>" y el líder "lider01"
    Then debe lanzarse un error de validación con mensaje "<mensaje>"

    Examples:
      | nombre | mensaje               |
      | AB     | al menos 3 caracteres |
      | X      | al menos 3 caracteres |

  Scenario: Agregar un objeto no válido como tarea lanza error
    Given que existe el proyecto "Proyecto QA" con el líder "lider01"
    When intento agregar "esto no es una tarea" al proyecto "Proyecto QA"
    Then debe lanzarse un error de validación con mensaje "tipo Tarea"

  # ── Edge Cases ───────────────────────────────────────────────────────────────

  Scenario: Filtrar tareas por prioridad retorna solo las coincidentes
    Given que existe el proyecto "Filtrado" con el líder "lider01"
    And el proyecto "Filtrado" tiene una tarea "Tarea urgente" con prioridad "ALTA"
    And el proyecto "Filtrado" tiene una tarea "Tarea normal" con prioridad "BAJA"
    When filtro las tareas del proyecto "Filtrado" por prioridad "ALTA"
    Then debo obtener 1 tarea con prioridad "ALTA"

  Scenario: Crear proyecto sin líder es válido
    When creo un proyecto llamado "Proyecto Solo" sin líder
    Then el proyecto "Proyecto Solo" debe existir
    And el líder del proyecto debe ser nulo
