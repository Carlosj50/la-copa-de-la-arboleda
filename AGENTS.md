# AGENTS

Ultima actualizacion: 29-03-2026

## Proposito

Este archivo define las reglas de trabajo para cualquier agente, IA o colaborador tecnico que intervenga en el repositorio.

## Regla principal

Trabajar en modo spec-driven de verdad:

- primero entender la especificacion
- despues cambiar datos o codigo
- por ultimo reflejar el estado operativo

## Capas de verdad

- `docs/`: contrato de diseno y especificacion tecnica
- `data/world`: contenido operativo del juego
- `STATE.md`: estado real del repositorio

No mezclar estas capas por comodidad.

## Reglas obligatorias

1. No improvisar arquitectura.
2. No cambiar la tecnologia nuclear del proyecto.
3. No introducir dependencias externas sin justificarlas.
4. No convertir el parser en NLP libre.
5. No hardcodear la aventura dentro del bucle principal.
6. No ampliar el conjunto de condiciones o efectos sin documentarlo primero.
7. No introducir aliases de habitaciones que colisionen con objetos o fixtures de esa misma sala.
8. No resolver problemas de contenido metiendo excepciones ad hoc en el motor si pueden resolverse limpiando datos o especificacion.
9. Mantener cambios pequenos, trazables y faciles de revisar.

## Orden minimo de lectura antes de tocar algo estructural

1. `STATE.md`
2. `docs/DECISIONS.md`
3. `docs/REQUIREMENTS_V1.md`
4. `docs/GAME_DESIGN.md`
5. `docs/WORLD_MODEL.md`
6. `docs/DATA_FORMAT.md`
7. `docs/ARCHITECTURE.md`

## Regla de precedencia documental

Si una modificacion afecta parser, arquitectura, world model, formato de datos o diseno del juego:

1. actualizar primero la especificacion afectada en `docs/`
2. resumir la decision en `docs/DECISIONS.md`
3. sincronizar `data/world` o el codigo
4. reflejar el nuevo punto de situacion en `STATE.md`

## Criterios de calidad

- claridad antes que brillantez
- coherencia antes que cantidad
- mantenibilidad antes que trucos
- puzles logicos antes que arbitrariedad
- retro con sentido antes que nostalgia hueca

## Regla sobre ideas no previstas

Si aparece una idea interesante pero no necesaria para la fase en curso:

- documentarla como posibilidad futura
- no convertirla en decision inmediata
- no ampliar el alcance sin dejar constancia
