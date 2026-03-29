# World Model

Ultima actualizacion: 29-03-2026

## Objetivo

Definir el modelo conceptual minimo para representar el mundo del juego de forma clara, extensible y testeable sin convertirlo en una arquitectura excesiva.

## Definicion estatica del juego

### `GameDefinition`

Agrupa todo el contenido authored necesario para ejecutar una partida:

- metadatos del juego
- escena opcional de introduccion
- habitacion inicial
- flags iniciales
- habitaciones
- objetos
- interacciones especiales

### `RoomDefinition`

Representa una habitacion jugable.

Campos conceptuales:

- `id`
- `zone`
- `name`
- `aliases`
- `scene_id`
- `first_description`
- `repeat_description`
- `exits`
- `objects`
- `tags`
- `context_actions`
- `context_directions`
- `enter_events`

### `ExitDefinition`

Representa una conexion navegable entre habitaciones.

Campos conceptuales:

- `direction`
- `target`
- `conditions`
- `failure_text`

### `ObjectDefinition`

Representa cualquier entidad authored examinable o manipulable. El modelo no separa tecnicamente `objeto` y `fixture` en clases distintas; los diferencia por `kind`.

Campos conceptuales:

- `id`
- `name`
- `aliases`
- `kind`
- `portable`
- `listed`
- `location`
- `description`
- `read_text`
- `initial_visible`
- `initial_states`
- `on_examine_effects`
- `on_read_effects`
- `on_take_effects`

### `RoomEventDefinition`

Evento disparado al entrar en una habitacion.

Campos conceptuales:

- `conditions`
- `effects`
- `text`

### `InteractionDefinition`

Regla declarativa especial resuelta por el motor.

Campos conceptuales:

- `id`
- `action`
- `room_id`
- `direct_object`
- `indirect_object`
- `preposition`
- `conditions`
- `effects`
- `success_text`
- `failure_text`

## Tipos de objeto authored

### `main`

Objeto de progreso principal.

### `optional`

Pista o hallazgo opcional con impacto real en comprension o ritmo.

### `fixture`

Elemento fijo del entorno con el que el parser debe poder interactuar.

### `ambient`

Elemento atmosferico sin papel mecanico principal.

## Estado mutable de partida

### `GameState`

Representa el runtime de una partida.

Campos conceptuales:

- `current_room_id`
- `inventory`
- `flags`
- `object_locations`
- `object_states`
- `visited_rooms`
- `game_over`
- `exit_requested`

## Flags comprometidas para V1

- `broken_fence_crossable`
- `front_shortcut_open`
- `tool_room_open`
- `lamp_filled`
- `lamp_lit`
- `pantry_hint_found`
- `portrait_clue_found`
- `library_history_found`
- `bedroom_letter_found`
- `medallion_found`
- `chapel_window_repaired`
- `chapel_mechanism_solved`
- `cup_revealed`
- `sacristy_open`
- `cellar_slab_open`
- `aljibe_crossed`
- `cup_filled`
- `grotto_open`
- `final_archive_open`

## Condiciones soportadas en V1

Conjunto cerrado:

- `flag_true`
- `flag_false`
- `inventory_contains`
- `inventory_not_contains`
- `object_state_is`
- `object_in_room`
- `current_room_is`

## Efectos soportados en V1

Conjunto cerrado:

- `set_flag`
- `set_object_state`
- `move_object`
- `reveal_object`
- `end_game`

## Reglas de modelado

- el parser no resuelve ids; solo produce tokens normalizados
- el motor resuelve tokens contra objetos visibles, fixtures e inventario
- una habitacion no debe tener aliases que pisen objetos locales
- los objetos criticos no deben depender de estados irreversibles punitivos
- las salidas se bloquean por condiciones, no por codigo oculto repartido

## Variante de final

La variante de final depende de flags opcionales de comprension:

- `portrait_clue_found`
- `library_history_found`
- `bedroom_letter_found`

Con dos o mas activas, el cierre se amplia.
