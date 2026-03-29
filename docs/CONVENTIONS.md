# Conventions

Ultima actualizacion: 29-03-2026

## Nomenclatura

### Codigo Python

- modulos y archivos: `snake_case`
- clases: `PascalCase`
- funciones y variables: `snake_case`
- constantes: `UPPER_SNAKE_CASE`

### Datos

- ids de habitaciones, objetos y flags: `snake_case`
- nombres visibles al jugador: en espanol natural

### Documentacion

- idioma: espanol
- fechas: `DD-MM-YYYY`

## Idioma de codigo frente a idioma del juego

Decision operativa:

- codigo y tipos internos: preferentemente en ingles tecnico simple
- textos mostrados al jugador: en espanol
- ids de contenido: `snake_case` sin acentos

Motivo:

- mantener legibilidad tecnica y evitar problemas con claves y normalizacion

## Organizacion de carpetas

- `docs/`: especificaciones y referencia de diseno
- `src/game/engine`: coordinacion del runtime
- `src/game/parser`: analisis de comandos
- `src/game/model`: tipos y dataclasses
- `src/game/content`: carga y validacion de datos
- `src/game/persistence`: saves
- `src/game/shared`: utilidades neutrales
- `data/world`: contenido authored
- `data/saves`: partidas guardadas
- `tests`: pruebas automatizadas

Regla documental:

- `docs/` define la spec
- `STATE.md` registra el estado operativo
- `data/world` refleja el contenido ejecutable

## Estilo Python

- tipado cuando aclare la intencion
- `dataclass` para estructuras de datos claras
- `Enum` solo cuando limite un conjunto cerrado util
- evitar jerarquias profundas de herencia
- evitar metaprogramacion

## Comentarios

- pocos y utiles
- explicar decisiones o bloques no evidentes
- no comentar obviedades

## Limites de tamano recomendados

- modulo de motor: idealmente hasta 300 lineas
- modulo de parser: idealmente hasta 250 lineas
- funciones individuales: preferencia por bloques cortos y legibles
- si un archivo supera claramente el tamano razonable, dividir por responsabilidad

## Separacion entre logica y contenido

- el motor no define textos de habitaciones
- el contenido no ejecuta codigo arbitrario
- la logica especial debe expresarse con handlers conocidos e ids de datos
- los aliases deben revisarse como parte del contenido, no como detalle cosmetico

## Convencion de aliases

- no reutilizar en una habitacion un alias de sala para un objeto o fixture local
- evitar aliases demasiado genericos en ambientales si existe un objeto principal cercano

## Convenciones de tipado y estructuras

- usar `dataclass` para entidades centrales del dominio
- reservar `TypedDict` o dicts puros para carga intermedia de JSON si aporta claridad
- convertir datos crudos a objetos de dominio cuanto antes en el flujo

## Convencion de cambios

- cambios pequenos
- un motivo claro por cambio
- actualizar documentacion si cambia comportamiento
