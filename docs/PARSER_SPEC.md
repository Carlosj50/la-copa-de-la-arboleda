# Parser Spec

Ultima actualizacion: 29-03-2026

## Alcance de V1

El parser V1 es corto, determinista y deliberadamente limitado. Su funcion es traducir comandos simples del jugador a acciones estructuradas del motor.

## Normalizacion de entrada

Antes de analizar un comando, el parser debe:

1. recortar espacios iniciales y finales
2. pasar el texto a mayusculas o a una forma normalizada equivalente
3. eliminar signos de puntuacion irrelevantes
4. eliminar tildes para comparacion
5. comprimir espacios multiples
6. normalizar alias y sinonimos

Ejemplos:

- `que ves?` -> `MIRAR`
- `ver cuaderno` -> `EXAMINAR CUADERNO`
- `n` -> `NORTE`

## Gramatica soportada

### G1. Verbo

Forma:

- `VERBO`

Ejemplos:

- `MIRAR`
- `INVENTARIO`
- `AYUDA`
- `FIN`

### G2. Direccion

Forma:

- `DIRECCION`

Ejemplos:

- `NORTE`
- `ABAJO`

### G3. Verbo + direccion

Forma:

- `VERBO DIRECCION`

Ejemplos:

- `IR NORTE`
- `IR ABAJO`

### G4. Verbo + objeto

Forma:

- `VERBO OBJETO`

Ejemplos:

- `LEER CUADERNO`
- `COGER LAMPARA`

### G5. Verbo + objeto + preposicion + objeto

Forma:

- `VERBO OBJETO PREPOSICION OBJETO`

Ejemplos:

- `USAR LLAVE EN PUERTA`
- `USAR ACEITE EN LAMPARA`
- `USAR COPA EN CUENCO`

## Preposiciones admitidas en V1

- `EN`
- `CON`
- `A`

`AL` se normaliza a `A`.

## Resolucion de objetos

El parser no decide por si solo si una accion es valida. Solo normaliza la entrada y produce un comando estructurado.

Reglas:

- la resolucion contra ids y visibilidad ocurre en el motor
- el motor intenta casar el texto contra objetos visibles, fixtures e inventario
- si hay cero candidatos, se informa al jugador
- si hay mas de un candidato, se pide mas precision

Regla de autoria:

- el contenido debe evitar alias criticos que colisionen innecesariamente
- una habitacion no debe usar aliases que pisen fixtures locales

## Estructura prevista del comando parseado

Campos minimos:

- `action`
- `raw_text`
- `direct_text`
- `indirect_text`
- `preposition`
- `direction`
- `error_message`

## Errores del parser

### Entrada vacia

Respuesta sugerida:

- "No has escrito ningun comando."

### Verbo no reconocido

Respuesta sugerida:

- "No entiendo ese verbo."

### Forma no soportada

Respuesta sugerida:

- "Ese formato no esta soportado en esta version."

### Ambiguedad

Respuesta sugerida:

- "Hay mas de una interpretacion posible. Se mas concreto."

### Objeto desconocido

Respuesta sugerida:

- "No identifico ese objeto."

## Respuestas amigables

El parser debe ser seco pero no hostil.

Buenas propiedades:

- una sola idea por mensaje
- sin tecnicismos internos
- sin culpar al jugador

## Lo que no soporta V1

- frases largas de lenguaje natural
- varias acciones en una linea
- referencias pronominales encadenadas
- correcciones automaticas agresivas
- analisis sintactico complejo
- inferencias semanticas no documentadas

## Comando especial de salida de sesion

Para evitar conflicto con `SALIR` como verbo del mundo:

- `FIN` cierra la sesion
- `SALIR JUEGO` tambien puede aceptarse como forma explicita
