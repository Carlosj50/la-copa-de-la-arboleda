# Architecture

Ultima actualizacion: 29-03-2026

## Objetivo arquitectonico

Construir un motor pequeno, legible y modular para una aventura conversacional de consola, manteniendo separadas las responsabilidades clave del proyecto.

## Principios

- Motor simple antes que framework casero.
- Contenido separado de la logica de ejecucion.
- Parser pequeno y determinista.
- Modelo del mundo explicito y testeable.
- Persistencia local en formato legible.
- Sin metaprogramacion innecesaria.

## Estructura prevista de modulos

### `src/game/engine`

Responsable de:

- bucle principal
- coordinacion de estado
- resolucion de acciones
- navegacion
- aplicacion de efectos
- validacion runtime basica

### `src/game/parser`

Responsable de:

- normalizacion de entrada
- tokenizacion sencilla
- resolucion de forma gramatical
- produccion de un comando estructurado
- mensajes de error de parseo

### `src/game/model`

Responsable de:

- dataclasses y enums de dominio
- definicion de rooms, objects, exits, commands y state
- tipos compartidos entre parser, motor y persistencia

### `src/game/content`

Responsable de:

- carga de datos del mundo
- adaptacion de JSON a modelo Python
- validaciones de integridad de contenido
- acceso a textos authored

### `src/game/persistence`

Responsable de:

- guardar estado a JSON
- cargar estado desde JSON
- validaciones basicas de version y consistencia

### `src/game/shared`

Responsable de:

- utilidades pequenas y neutras
- helpers de texto
- constantes compartidas

## Flujo principal previsto

1. Arranque del programa.
2. Carga de contenido desde `data/world`.
3. Construccion del `GameDefinition`.
4. Creacion de `GameState` nuevo o carga desde save.
5. Render de la situacion actual.
6. Lectura de comando del jugador.
7. Parseo a comando estructurado.
8. Resolucion del comando contra mundo y estado.
9. Aplicacion de efectos y mensajes.
10. Persistencia si procede.
11. Repeticion del bucle hasta salir o finalizar.

## Relacion entre contenido y motor

Regla central:

- El motor conoce tipos, reglas y handlers.
- El contenido conoce habitaciones, objetos, fixtures, textos, flags iniciales e interacciones declaradas.

El motor no debe contener:

- textos completos de habitaciones
- mapa hardcodeado
- listas de objetos del juego incrustadas en el bucle principal

El contenido no debe contener:

- codigo Python arbitrario ejecutado dinamicamente
- reglas opacas fuera del conjunto de handlers previstos

Regla adicional:

- V1 usa un conjunto cerrado de condiciones y efectos
- no se introduce una DSL abierta de reglas

## Estrategia de persistencia

V1 guardara en JSON:

- habitacion actual
- inventario
- flags del mundo
- ubicacion de objetos
- estados de objetos
- habitaciones visitadas

No se guardaran caches ni derivados faciles de recomputar.

## Fuente de verdad

- `docs/` conserva la referencia de diseno
- `data/world` conserva la referencia operativa del contenido
- `STATE.md` resume el estado real del repositorio

Si estas capas divergen, debe corregirse la discrepancia de inmediato.

## Validacion prevista

Antes de ejecutar una partida, el cargador deberia poder comprobar:

- ids unicos
- exits hacia habitaciones existentes
- objetos referenciados existentes
- flags declaradas validas
- interacciones con handlers conocidos
- condiciones y efectos soportados
- colisiones locales de aliases
- acciones contextuales apuntando a salidas validas

## Escenas pixeladas de consola

La version actual admite una capa visual opcional y contenida:

- `world.json` puede declarar una `intro_scene`
- cada habitacion puede declarar un campo opcional `scene`
- el render de escenas vive aislado en `shared/pixel_art.py`
- el motor sigue siendo de consola y el texto conserva prioridad

Reglas de esta capa:

- las escenas son estaticas
- no hay GUI ni ventana grafica
- no hay impacto en parser ni logica de puzles
- si una escena falta, la habitacion sigue siendo jugable por texto
