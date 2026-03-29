# Data Format

Ultima actualizacion: 29-03-2026

## Objetivo

Definir una estrategia de datos simple, robusta y legible para representar el mundo y los saves en V1.

## Decision base

Formato preferido para V1:

- JSON para contenido
- JSON para saves

Motivos:

- lectura sencilla
- escritura sencilla desde stdlib
- integracion natural con Python
- validacion simple

## Distribucion de archivos

```text
data/
  world/
    world.json
    rooms.json
    objects.json
    interactions.json
  saves/
    slot_001.json
```

## Principio de schema

No se adopta una DSL abierta. V1 solo admite un conjunto cerrado de estructuras, condiciones y efectos documentados.

## `world.json`

Contiene:

- `title`
- `data_version`
- `intro_scene`
- `start_room`
- `intro`
- `initial_flags`

Ejemplo:

```json
{
  "title": "La Copa de la Arboleda",
  "data_version": 1,
  "intro_scene": "intro_carpeta",
  "start_room": "camino_entrada",
  "intro": [
    "Texto de introduccion."
  ],
  "initial_flags": {
    "broken_fence_crossable": false,
    "lamp_lit": false
  }
}
```

## `rooms.json`

Cada entrada representa una `RoomDefinition`.

Campos:

- `id`
- `zone`
- `name`
- `aliases`
- `scene`
- `first_description`
- `repeat_description`
- `exits`
- `objects`
- `tags`
- `context_actions`
- `context_directions`
- `enter_events`

Ejemplo:

```json
{
  "id": "patio_exterior",
  "zone": "zona_2",
  "name": "Patio exterior",
  "aliases": ["patio frontal"],
  "scene": "patio_exterior",
  "first_description": "Texto de primera entrada.",
  "repeat_description": "Texto breve de revisitacion.",
  "exits": {
    "OESTE": {
      "target": "sendero_piedras",
      "conditions": [
        {"type": "flag_true", "name": "front_shortcut_open"}
      ],
      "failure_text": "La verja frontal aun no puede abrirse desde aqui."
    },
    "ESTE": {
      "target": "vestibulo"
    }
  },
  "objects": ["puerta_aperos"],
  "tags": ["exterior", "hub"],
  "context_actions": {
    "ENTRAR": "ESTE"
  },
  "enter_events": [
    {
      "conditions": [
        {"type": "flag_false", "name": "front_shortcut_open"}
      ],
      "effects": [
        {"type": "set_flag", "name": "front_shortcut_open", "value": true}
      ],
      "text": "El acceso frontal queda destrancado desde dentro."
    }
  ]
}
```

Notas:

- `intro_scene` es opcional y referencia una escena estatica de consola conocida por el motor
- `scene` es opcional por habitacion y sigue la misma regla
- estas escenas no afectan parser, estado ni persistencia

## `objects.json`

Cada entrada representa un `ObjectDefinition`.

Campos:

- `id`
- `name`
- `aliases`
- `kind`
- `portable`
- `listed`
- `location`
- `description`
- `read_text`
- `visible`
- `states`
- `on_examine_effects`
- `on_read_effects`
- `on_take_effects`

`kind` admite:

- `main`
- `optional`
- `fixture`
- `ambient`

Ejemplo:

```json
{
  "id": "lampara_aceite",
  "name": "lampara de aceite",
  "aliases": ["lampara"],
  "kind": "main",
  "portable": true,
  "listed": true,
  "location": "dormitorio_familiar",
  "description": "Una lampara vieja.",
  "states": {
    "filled": false,
    "lit": false
  }
}
```

Ejemplo de fixture:

```json
{
  "id": "roseton_capilla",
  "name": "roseton",
  "aliases": ["ventana"],
  "kind": "fixture",
  "portable": false,
  "listed": false,
  "location": "capilla_ruinas",
  "description": "Le falta una pieza."
}
```

## `interactions.json`

Cada entrada representa una `InteractionDefinition`.

Campos:

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

Ejemplo:

```json
{
  "id": "usar_tabla_en_zanja",
  "action": "USAR",
  "room_id": "valla_rota",
  "direct_object": "tabla_suelta",
  "indirect_object": "zanja_barro",
  "conditions": [
    {"type": "inventory_contains", "object_id": "tabla_suelta"},
    {"type": "flag_false", "name": "broken_fence_crossable"}
  ],
  "effects": [
    {"type": "set_flag", "name": "broken_fence_crossable", "value": true},
    {"type": "move_object", "object_id": "tabla_suelta", "location": "valla_rota"},
    {"type": "set_object_state", "object_id": "tabla_suelta", "state": "fixed", "value": true}
  ],
  "success_text": "La tabla queda fija sobre la zanja."
}
```

## Condiciones soportadas

- `flag_true`
- `flag_false`
- `inventory_contains`
- `inventory_not_contains`
- `object_state_is`
- `object_in_room`
- `current_room_is`

## Efectos soportados

- `set_flag`
- `set_object_state`
- `move_object`
- `reveal_object`
- `end_game`

Regla:

- no existe `open_exit`
- una salida se habilita mediante flags o condiciones declaradas en la propia salida

## Formato de save

El save refleja solo estado mutable.

Campos:

- `save_version`
- `current_room`
- `inventory`
- `flags`
- `object_locations`
- `object_states`
- `visited_rooms`

Ejemplo:

```json
{
  "save_version": 1,
  "current_room": "cocina",
  "inventory": ["lampara_aceite", "caja_cerillas"],
  "flags": {
    "broken_fence_crossable": true,
    "lamp_lit": false
  },
  "object_locations": {
    "lampara_aceite": "__inventory__",
    "tabla_suelta": "valla_rota"
  },
  "object_states": {
    "lampara_aceite": {
      "visible": true,
      "filled": true,
      "lit": false
    }
  },
  "visited_rooms": ["camino_entrada", "cruce_bosque"]
}
```

## Reglas de formato

- ids en `snake_case`
- claves estables y sin acentos
- textos del jugador separados de reglas
- nada de codigo ejecutable embebido en datos
- los aliases deben revisarse como parte del contenido, no como detalle menor
