# Requisitos V1

Ultima actualizacion: 29-03-2026

## Objetivo de V1

Entregar una aventura conversacional completa, jugable en consola, con un mundo cerrado y coherente, parser limitado, persistencia minima y contenido desacoplado del motor.

## Requisitos funcionales

### RF-01. Inicio de partida

El juego debe permitir iniciar una partida nueva desde consola y situar al jugador en la habitacion inicial con contexto narrativo suficiente.

### RF-02. Bucle principal

El juego debe ejecutar un bucle principal que:

- muestre informacion relevante
- reciba un comando
- lo analice
- lo resuelva
- actualice el estado
- devuelva una respuesta clara

### RF-03. Movimiento

El jugador debe poder desplazarse por un mapa de 24 habitaciones conectadas de forma coherente.

### RF-04. Observacion y examen

El jugador debe poder:

- mirar la habitacion actual
- examinar objetos y fixtures visibles
- leer textos relevantes
- consultar salidas y elementos visibles de forma natural

### RF-05. Interaccion con objetos

El sistema debe soportar:

- coger
- soltar
- usar
- abrir
- cerrar
- empujar
- tirar
- leer
- encender
- apagar

siempre dentro del conjunto limitado definido por el parser V1.

### RF-06. Inventario

El jugador debe disponer de inventario y poder consultar, examinar y usar los objetos transportados.

### RF-07. Estado del mundo

El juego debe modelar como minimo:

- habitaciones
- salidas condicionadas
- objetos authored
- fixtures interactivos
- inventario
- flags del mundo
- estados de objetos
- eventos de entrada
- acciones contextuales de movimiento cuando proceda

### RF-08. Progresion principal

La aventura debe incluir 9 hitos principales de progresion:

- 8 puzles mecanicos o espaciales
- 1 hito principal de interpretacion

La aventura debe evitar inflar el recuento llamando puzle a cada hallazgo narrativo.

### RF-09. Desvios opcionales

La aventura debe incluir 3 desvios opcionales de valor real:

- al menos 1 con resolucion jugable propia
- el resto pueden ser capas de pista o comprension

Los desvios opcionales no deben bloquear el flujo principal.

### RF-10. Finales

El juego debe ofrecer:

- 1 final principal
- 1 variante de final basada en el nivel de comprension y pistas reunidas

### RF-11. Persistencia

El jugador debe poder guardar y cargar una partida desde almacenamiento local.

### RF-12. Contenido desacoplado

El contenido del mundo no debe quedar incrustado de forma caotica en el bucle principal. Debe cargarse desde datos o estructuras claramente separadas.

### RF-13. Validacion de contenido

Antes de ejecutar una partida, el proyecto debe poder detectar como minimo:

- referencias a habitaciones inexistentes
- referencias a objetos inexistentes
- flags no declaradas
- condiciones o efectos no soportados
- colisiones locales entre aliases de habitacion y objetos visibles

## Requisitos no funcionales

### RNF-01. Tecnologia

- Python 3.12 como objetivo
- prioridad de biblioteca estandar
- dependencias externas minimizadas

### RNF-02. Plataforma inicial

- Windows como plataforma principal
- ejecucion desde terminal/consola
- entorno virtual local en `.venv`

### RNF-03. Mantenibilidad

- codigo modular
- nombres claros
- separacion entre parser, motor, modelo, contenido y persistencia
- archivos de tamano razonable

### RNF-04. Testabilidad

Las piezas clave deben poder validarse de manera automatizada:

- parser
- movimiento
- inventario
- flags
- eventos
- guardado/carga
- integridad de contenido

### RNF-05. Sencillez operativa

No se requieren optimizaciones complejas. La prioridad es que el juego arranque rapido, cargue datos pequenos y mantenga una estructura simple.

## Restricciones

- no usar motor grafico
- no convertir el proyecto en app web
- no usar parser de NLP libre
- no introducir mapa automatico
- no depender de tecnologias fuera de alcance para V1
- no construir una DSL de reglas abierta o arbitraria

## Casos de uso basicos

### CU-01. Explorar

Como jugador quiero moverme entre habitaciones y recibir descripciones claras para construir un mapa mental.

### CU-02. Inspeccionar

Como jugador quiero examinar lugares, objetos y fixtures para reunir pistas utiles.

### CU-03. Resolver puzles

Como jugador quiero usar objetos y conocimiento del mundo para desbloquear nuevas zonas.

### CU-04. Guardar progreso

Como jugador quiero guardar y cargar partida para retomar la exploracion sin perder avance.

### CU-05. Entender el misterio

Como jugador quiero descubrir el secreto central de la finca a traves de la exploracion y las notas del familiar.

## Definition of Done de V1

V1 se considerara terminada cuando:

- el juego completo sea jugable de principio a fin
- las 24 habitaciones esten implementadas
- el flujo principal pueda resolverse sin bloqueos
- los hitos principales y opcionales respondan con coherencia
- exista guardado y carga funcional
- el parser V1 soporte el lexico especificado
- el contenido este desacoplado del bucle principal
- haya validacion de contenido para referencias, flags y aliases locales
- haya pruebas automatizadas para los comportamientos base
- la documentacion refleje lo realmente implementado
