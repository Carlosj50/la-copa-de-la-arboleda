# Decisions

Ultima actualizacion: 29-03-2026

## DEC-001

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: Python 3.12 como lenguaje objetivo.
- Motivo: encaja con el alcance, permite stdlib suficiente, facilita tipado y dataclasses sin complejidad gratuita.
- Consecuencia: cualquier propuesta tecnica debe justificarse dentro del ecosistema Python.

## DEC-002

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: entorno virtual local en `.venv` dentro de la raiz del proyecto.
- Motivo: visibilidad, simplicidad operativa y coherencia con el flujo de trabajo en Windows.
- Consecuencia: el runbook y los scripts futuros asumiran esta ubicacion.

## DEC-003

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: consola como interfaz inicial y unica interfaz comprometida para V1.
- Motivo: alinea el proyecto con su identidad retro y mantiene el foco tecnico.
- Consecuencia: no se disena ninguna capa visual moderna en esta etapa.

## DEC-004

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: no usar motor grafico, SPA, Electron ni frontend web.
- Motivo: estan fuera del alcance y desalinean la experiencia buscada.
- Consecuencia: cualquier propuesta visual futura debera ser estatica, auxiliar y no intrusiva.

## DEC-005

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: parser controlado, de gramatica limitada.
- Motivo: se prioriza fiabilidad, mantenibilidad y justicia sobre falsa inteligencia.
- Consecuencia: las formas aceptadas deben quedar documentadas y probadas.

## DEC-006

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: disenar el juego completo desde el inicio.
- Motivo: evita crecimiento caotico y permite que motor, contenido y puzles nazcan alineados.
- Consecuencia: los cambios estructurales del mundo requeriran actualizacion de la documentacion maestra.

## DEC-007

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: separar motor, parser, modelo, contenido, persistencia y utilidades compartidas.
- Motivo: reduce acoplamiento y facilita pruebas.
- Consecuencia: se evitara hardcodear la aventura entera en el bucle principal.

## DEC-008

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: prioridad de biblioteca estandar y formato JSON para datos y saves en V1.
- Motivo: JSON es legible, escribible desde stdlib y suficiente para el tamano del proyecto.
- Consecuencia: TOML queda como posibilidad solo para configuracion futura, no como formato principal de contenido mutable en V1.

## DEC-009

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: no introducir consumo, temporizadores opacos ni callejones sin salida punitivos en el flujo principal.
- Motivo: la dificultad debe venir de la observacion y deduccion, no del castigo arbitrario.
- Consecuencia: los puzles y estados del mundo se disenan para ser reversibles y validables.

## DEC-010

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: permitir escenas pixeladas estaticas dentro de la propia consola para portada y habitaciones seleccionadas.
- Motivo: aporta atmosfera visible sin romper el enfoque retro, sin GUI y sin convertir el proyecto en una aventura visual moderna.
- Consecuencia: el soporte visual queda aislado, es opcional por habitacion y no altera parser, puzles ni persistencia.

## DEC-011

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: modelar `fixture` como tipo de objeto authored dentro del mismo modelo base.
- Motivo: evita una jerarquia innecesaria y permite que parser, contenido y validacion hablen un lenguaje comun.
- Consecuencia: `objects.json` admite `kind = fixture` y la documentacion lo trata como entidad de primer nivel.

## DEC-012

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: mantener un conjunto cerrado de condiciones y efectos declarativos en V1.
- Motivo: reduce la tentacion de convertir el contenido en una DSL abierta o en logica opaca.
- Consecuencia: ampliar estos conjuntos exige actualizar antes `docs/WORLD_MODEL.md`, `docs/DATA_FORMAT.md` y los validadores.

## DEC-013

- Fecha: 29-03-2026
- Estado: aceptada
- Decision: separar explicitamente especificacion, estado operativo y fuente de datos ejecutable.
- Motivo: evita mezclar diseno, seguimiento e implementacion hasta volverlos indistinguibles.
- Consecuencia: `docs/` conserva la referencia de diseno, `STATE.md` resume el build real y `data/world` actua como verdad operativa del contenido.
