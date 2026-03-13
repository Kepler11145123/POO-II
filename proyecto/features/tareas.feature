Feature: Gestión de Tareas
  Como miembro del equipo
  Quiero gestionar el ciclo de vida de las tareas
  Para hacer seguimiento del progreso del trabajo

  Background:
    Given que el sistema está inicializado

  # ── Happy Path ───────────────────────────────────────────────────────────────

  Scenario: Crear una tarea con título y prioridad válidos
    When creo una tarea con título "Implementar login" y prioridad "ALTA"
    Then la tarea debe existir con título "Implementar login"
    And la tarea debe estar en estado "PENDIENTE"

  Scenario: Iniciar una tarea pendiente
    Given que existe una tarea "Revisar código" con prioridad "MEDIA"
    When inicio la tarea "Revisar código"
    Then la tarea "Revisar código" debe estar en estado "EN_PROGRESO"

  Scenario: Completar una tarea
    Given que existe una tarea "Escribir tests" con prioridad "ALTA"
    When completo la tarea "Escribir tests"
    Then la tarea "Escribir tests" debe estar en estado "COMPLETADA"
    And la tarea "Escribir tests" debe tener fecha de completado registrada

  # ── Escenario de error ───────────────────────────────────────────────────────

  Scenario Outline: Crear tarea con título inválido lanza error
    When intento crear una tarea con título "<titulo>"
    Then debe lanzarse un error de validación con mensaje "<mensaje>"

    Examples:
      | titulo | mensaje               |
      | AB     | al menos 3 caracteres |
      | T      | al menos 3 caracteres |
      |        | al menos 3 caracteres |

  # ── Edge Cases ───────────────────────────────────────────────────────────────

  Scenario Outline: Cambiar la prioridad de una tarea
    Given que existe una tarea "Tarea flexible" con prioridad "BAJA"
    When cambio la prioridad de la tarea "Tarea flexible" a "<nueva_prioridad>"
    Then la tarea "Tarea flexible" debe tener prioridad "<nueva_prioridad>"

    Examples:
      | nueva_prioridad |
      | ALTA            |
      | MEDIA           |
      | BAJA            |

  Scenario: Completar una tarea directamente desde pendiente sin iniciarla
    Given que existe una tarea "Tarea directa" con prioridad "BAJA"
    When completo la tarea "Tarea directa"
    Then la tarea "Tarea directa" debe estar en estado "COMPLETADA"

  Scenario: Crear tarea sin descripción ni prioridad es válido
    When creo una tarea con título "Tarea mínima" sin descripción ni prioridad
    Then la tarea debe existir con título "Tarea mínima"
    And la prioridad de la tarea debe ser nula
