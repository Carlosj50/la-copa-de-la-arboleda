# Command Lexicon

Ultima actualizacion: 29-03-2026

## Objetivo

Definir el lexico aceptado por el parser V1 para evitar ambiguedad, falsas expectativas y crecimiento caotico.

## Principios

- El parser acepta pocas formas, pero de forma fiable.
- Los alias existen para suavizar la entrada, no para abrir NLP libre.
- Los objetos y salidas deben responder de forma coherente con el mundo visible.

## Verbos canonicos

### MIRAR

- Canonico: `MIRAR`
- Alias aceptados: `MIRA`, `VER`, `OBSERVAR`, `OBSERVA`, `QUE VES`, `QUE VES?`
- Uso principal: describir la habitacion actual

### EXAMINAR

- Canonico: `EXAMINAR`
- Alias aceptados: `EXAMINA`, `INSPECCIONAR`, `VER` cuando hay objeto directo
- Uso principal: obtener detalle sobre un objeto o elemento concreto

### IR

- Canonico: `IR`
- Alias aceptados: direccion directa sin verbo, `AVANZAR`
- Uso principal: moverse

### ENTRAR

- Canonico: `ENTRAR`
- Alias aceptados: `ENTRA`
- Uso principal: acceder a una salida de entrada obvia o contextual

### SALIR

- Canonico: `SALIR`
- Alias aceptados: ninguno imprescindible en V1
- Uso principal: abandonar un espacio cuando la salida contextual es clara

### COGER

- Canonico: `COGER`
- Alias aceptados: `COGE`, `TOMAR`, `TOMA`, `RECOGER`, `RECOGE`
- Uso principal: mover objeto portable al inventario

### SOLTAR

- Canonico: `SOLTAR`
- Alias aceptados: `SUELTA`, `DEJAR`, `DEJA`
- Uso principal: dejar un objeto del inventario en la habitacion actual

### ABRIR

- Canonico: `ABRIR`
- Alias aceptados: `ABRE`
- Uso principal: abrir puertas, cajones o mecanismos preparados

### CERRAR

- Canonico: `CERRAR`
- Alias aceptados: `CIERRA`
- Uso principal: cerrar elementos que lo permitan

### USAR

- Canonico: `USAR`
- Alias aceptados: `USA`, `PONER`, `PON`
- Uso principal: interaccion instrumental con o sin objeto indirecto

### EMPUJAR

- Canonico: `EMPUJAR`
- Alias aceptados: `EMPUJA`
- Uso principal: desplazar o accionar algo por fuerza directa

### TIRAR

- Canonico: `TIRAR`
- Alias aceptados: `TIRA`
- Uso principal: tirar de cuerdas, anillas o paneles

### LEER

- Canonico: `LEER`
- Alias aceptados: `LEE`
- Uso principal: leer cuaderno, placa o documentos

### ENCENDER

- Canonico: `ENCENDER`
- Alias aceptados: `ENCIENDE`
- Uso principal: activar fuentes de luz u otros elementos encendibles

### APAGAR

- Canonico: `APAGAR`
- Alias aceptados: `APAGA`
- Uso principal: apagar una fuente de luz

### INVENTARIO

- Canonico: `INVENTARIO`
- Alias aceptados: `INV`, `I`
- Uso principal: listar objetos transportados

### AYUDA

- Canonico: `AYUDA`
- Alias aceptados: ninguno imprescindible en V1
- Uso principal: mostrar comandos base y orientacion mecanica minima

### GUARDAR

- Canonico: `GUARDAR`
- Alias aceptados: `GUARDA`
- Uso principal: persistir partida

### CARGAR

- Canonico: `CARGAR`
- Alias aceptados: `CARGA`
- Uso principal: recuperar partida guardada

### SALIR DEL JUEGO

- Canonico: `SALIR JUEGO`
- Alias aceptados: `FIN`
- Uso principal: abandonar la sesion sin interferir con `SALIR` como accion contextual de movimiento

## Direcciones y alias

- `NORTE` / `N`
- `SUR` / `S`
- `ESTE` / `E`
- `OESTE` / `O`
- `ARRIBA`
- `ABAJO`

Alias contextuales, solo si el contenido los define con claridad:

- `IZQUIERDA`
- `DERECHA`

Regla:

- `IZQUIERDA` y `DERECHA` no deben usarse como atajo universal si generan confusion espacial.
- solo deben funcionar si la habitacion define `context_directions`

## Formas aceptadas

### Forma 1. Solo verbo

Ejemplos:

- `MIRAR`
- `INVENTARIO`
- `AYUDA`
- `FIN`

### Forma 2. Direccion sola

Ejemplos:

- `NORTE`
- `ABAJO`

### Forma 3. Verbo + direccion

Ejemplos:

- `IR NORTE`
- `ENTRAR`
- `SALIR`

Regla:

- `ENTRAR` y `SALIR` solo deben depender de `context_actions` cuando la salida contextual sea obvia

### Forma 4. Verbo + objeto

Ejemplos:

- `EXAMINAR CUADERNO`
- `COGER COPA`
- `LEER PLACA`

### Forma 5. Verbo + objeto + preposicion + objeto

Preposiciones previstas en V1:

- `EN`
- `CON`
- `A`

Ejemplos:

- `USAR LLAVE EN PUERTA`
- `USAR ACEITE EN LAMPARA`
- `USAR COPA EN CUENCO`

## Respuestas por defecto

### Verbo desconocido

- "No entiendo ese verbo."

### Falta objeto

- "Te falta concretar que quieres usar."

### Objeto no visible ni transportado

- "No ves eso aqui."

### Objeto ambiguo

- "Hay mas de una cosa que podria encajar. Se mas concreto."

### Accion valida pero no posible

- "Ahora mismo eso no sirve."

### Falta requisito

- "Asi no consigues nada."

### Salida cerrada o bloqueada

- "Por ahi no puedes pasar."

## Limites explicitos de V1

El lexico V1 no promete:

- frases libres largas
- comandos encadenados
- pronombres complejos tipo "cogelo"
- adverbios relevantes
- dialogos avanzados con PNJ

## Regla de autoria sobre nombres

- el contenido debe evitar que una habitacion use aliases que pisen objetos o fixtures locales
- un ambiental no debe apropiarse del alias corto de un objeto critico

## Regla especial sobre `SALIR`

- `SALIR` se reserva para la accion contextual dentro del mundo.
- `SALIR JUEGO` o `FIN` se reserva para cerrar la sesion.
