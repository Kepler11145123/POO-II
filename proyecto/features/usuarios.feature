Feature: Gestión de Usuarios
  Como administrador del sistema
  Quiero gestionar los usuarios de la plataforma
  Para controlar el acceso y la participación en proyectos

  Background:
    Given que el sistema está inicializado

  # ── Happy Path ───────────────────────────────────────────────────────────────

  Scenario: Crear un usuario con datos válidos
    When creo un usuario con username "carlos99" y email "carlos@mail.com"
    Then el usuario debe existir con username "carlos99"
    And el usuario debe estar activo

  Scenario: Desactivar un usuario activo
    Given que existe un usuario con username "ana123" y email "ana@mail.com"
    When desactivo al usuario "ana123"
    Then el usuario "ana123" debe estar inactivo

  Scenario: Reactivar un usuario inactivo
    Given que existe un usuario con username "luis77" y email "luis@mail.com"
    And el usuario "luis77" está desactivado
    When activo al usuario "luis77"
    Then el usuario "luis77" debe estar activo

  # ── Escenario de error ───────────────────────────────────────────────────────

  Scenario Outline: Crear usuario con username inválido lanza error
    When intento crear un usuario con username "<username>" y email "test@mail.com"
    Then debe lanzarse un error de validación con mensaje "<mensaje>"

    Examples:
      | username  | mensaje               |
      | ab        | al menos 3 caracteres |
      | user_name | letras y números      |
      | us er     | letras y números      |

  Scenario: Crear usuario con email inválido lanza error
    When intento crear un usuario con username "valid99" y email "correo_invalido"
    Then debe lanzarse un error de validación con mensaje "Email inválido"

  # ── Edge Cases ───────────────────────────────────────────────────────────────

  Scenario: Crear usuario sin nombre completo es válido
    When creo un usuario con username "anonimo1" y email "anon@mail.com" sin nombre completo
    Then el usuario debe existir con username "anonimo1"
    And el nombre completo del usuario debe ser nulo

  Scenario: Desactivar un usuario ya inactivo no produce error
    Given que existe un usuario con username "beta99" y email "beta@mail.com"
    And el usuario "beta99" está desactivado
    When desactivo al usuario "beta99"
    Then el usuario "beta99" debe estar inactivo
