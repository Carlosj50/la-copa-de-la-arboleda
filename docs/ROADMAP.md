# Roadmap

Ultima actualizacion: 29-03-2026

## Regla de lectura

Este documento describe la secuencia comprometida del proyecto. El avance real de cada fase se consulta en `STATE.md`.

## Fase 0. Base documental

Objetivo:

- fijar vision
- cerrar requisitos
- disenar el mundo completo
- definir arquitectura y formato de datos
- preparar estructura base del proyecto

Criterio de salida:

- corpus documental coherente y util para construir

## Fase 1. Esqueleto tecnico

Objetivo:

- crear el paquete base en Python
- implementar parser basico V1
- definir modelo runtime del mundo
- cargar contenido desde datos
- crear bucle principal simple
- habilitar guardado y carga minimo

Criterio de salida:

- primera validacion jugable de estructura y flujo

## Fase 2. Integracion del contenido

Objetivo:

- trasladar el diseno del mundo a datos concretos
- escribir textos de habitaciones y objetos
- conectar eventos y puzles
- validar progresion principal y opcional

Criterio de salida:

- juego resoluble de principio a fin en modo texto

## Fase 3. Validacion y pruebas

Objetivo:

- ampliar pruebas del parser
- validar coherencia espacial
- comprobar estados de inventario y flags
- detectar errores de contenido y dependencias rotas

Criterio de salida:

- build interna estable para iteracion de pulido

## Fase 4. Pulido

Objetivo:

- ajustar textos
- suavizar respuestas del parser
- revisar dificultad y justicia de puzles
- mejorar mensajes de ayuda y errores

Criterio de salida:

- V1 candidata a version jugable estable

## Fase futura no comprometida

Posibles lineas posteriores, solo si se aprueban aparte:

- ampliar con criterio la cobertura de escenas pixeladas a mas habitaciones clave
- herramientas de validacion de contenido mas ricas
- utilidades de autor para ampliar el mundo sin tocar motor
