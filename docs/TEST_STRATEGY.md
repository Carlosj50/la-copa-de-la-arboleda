# Test Strategy

Ultima actualizacion: 29-03-2026

## Objetivo

Garantizar que el juego sea justo, coherente y mantenible validando tanto logica tecnica como integridad del contenido.

## Capas de validacion

### 1. Pruebas unitarias

Aplicadas a piezas pequenas:

- normalizacion del parser
- parseo de formas admitidas
- resolucion de direcciones
- operaciones de inventario
- cambios de flags
- serializacion y deserializacion de saves

### 2. Pruebas de integracion

Aplicadas a flujos cortos:

- abrir el cuarto de aperos con la llave
- rellenar y encender la lampara
- resolver el mecanismo de la capilla
- cruzar el aljibe
- abrir la gruta
- alcanzar el final principal

### 3. Validacion de contenido

Aplicada antes de jugar:

- ids unicos
- habitaciones existentes para cada salida
- objetos existentes para cada referencia
- flags conocidas
- ausencia de dependencias rotas en interacciones
- tipos de condicion y efecto soportados
- acciones contextuales apuntando a salidas validas
- ausencia de colisiones locales entre aliases de sala y objetos o fixtures

## Casos criticos a cubrir

### Parser

- alias basicos
- direcciones solas
- verbo con objeto
- verbo con objeto indirecto
- `ENTRAR` y `SALIR` contextuales
- entradas vacias o incorrectas

### Movimiento

- paso valido
- paso bloqueado
- atajos que se abren
- imposibilidad de cruzar antes de resolver un bloqueo

### Inventario

- coger objeto portable
- impedir coger objeto no portable
- soltar objeto
- usar objeto desde inventario

### Flags y eventos

- activar y leer flags
- disparar eventos de entrada
- respuestas correctas cuando falta requisito

### Guardado y carga

- guardar estado parcial
- recargar y recuperar habitacion, inventario y flags
- rechazar o advertir saves incompatibles por version

### Errores de contenido

- salida a sala inexistente
- referencia a objeto inexistente
- interaccion con handler no soportado
- flag no declarada
- alias de habitacion colisionando con fixture local

## Herramienta base recomendada

Para V1 se prioriza `unittest` de la biblioteca estandar.

Motivo:

- suficiente para el alcance
- sin dependencia extra
- facil de ejecutar en Windows

## Pruebas manuales recomendadas

Ademas de las automatizadas, conviene una pasada manual breve por build:

1. recorrido minimo hasta conseguir la copa
2. recorrido completo hasta el final principal
3. recorrido con al menos dos pistas opcionales para validar la variante
4. comprobacion de mensajes de error comunes

## Criterio minimo de estabilidad de V1

No deberia considerarse estable una build si no existen al menos:

- pruebas del parser basico
- pruebas de movimiento
- una prueba de guardado/carga
- una prueba de un puzle de extremo a extremo
- una validacion automatica del contenido authored
