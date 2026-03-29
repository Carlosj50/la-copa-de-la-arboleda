# Master Map

Ultima actualizacion: 29-03-2026

## Mapa global resumido

```text
Zona 1
1 Camino de entrada --E--> 2 Cruce del bosque
2 Cruce del bosque --N--> 3 Claro con pozo seco
2 Cruce del bosque --E--> 4 Sendero de piedras
3 Claro con pozo seco --E--> 5 Valla rota

Zona 2 y acceso a finca
4 Sendero de piedras --E--> 6 Patio exterior   [cerrado al inicio]
5 Valla rota --E--> 19 Patio trasero           [bloqueado al inicio]
6 Patio exterior --E--> 7 Vestibulo
6 Patio exterior --S--> 14 Cuarto de aperos
7 Vestibulo --N--> 8 Salon principal
7 Vestibulo --E--> 12 Biblioteca
8 Salon principal --E--> 9 Comedor
9 Comedor --S--> 10 Cocina
10 Cocina --E--> 11 Despensa
10 Cocina --S--> 19 Patio trasero
12 Biblioteca --N--> 13 Dormitorio del familiar

Zona 3
19 Patio trasero --E--> 17 Cobertizo
17 Cobertizo --E--> 18 Invernadero abandonado
19 Patio trasero --S--> 15 Capilla en ruinas
15 Capilla en ruinas --E--> 16 Sacristia       [cerrada al inicio]

Zona 4
16 Sacristia --ABAJO--> 20 Entrada al subterraneo [sellada al inicio]
20 Entrada al subterraneo --E--> 21 Pasillo de piedra
21 Pasillo de piedra --E--> 22 Camara del aljibe
22 Camara del aljibe --E--> 23 Gruta sellada   [bloqueada al inicio]
23 Gruta sellada --E--> 24 Camara final        [cerrada al inicio]
```

## Logica espacial

### Zona 1

El bosque actua como embudo inicial con dos lecturas:

- el sendero frontal conduce a la entrada elegante, pero cerrada
- el claro y la valla rota sugieren la via lateral, mas humilde y efectiva
- el sendero frontal anticipa el atajo principal que se abre mas adelante

### Zona 2

La casa principal se estructura como un circuito legible:

- frente y vestibulo
- eje salon-comedor-cocina
- eje vestibulo-biblioteca-dormitorio

La cocina conecta con el patio trasero y convierte la entrada lateral en acceso valido al interior.

### Zona 3

Los anexos reparten funciones:

- aperos: herramientas
- cobertizo: apoyo mecanico
- invernadero: hallazgo semienterrado y atmosfera humeda
- capilla: nucleo simbolico del misterio
- sacristia: transicion de lo visible a lo oculto

### Zona 4

El subsuelo estrecha la exploracion y concentra el final del juego en una cadena corta de salas con fuerte identidad:

- umbral
- corredor
- camara tecnica del agua
- puerta simbolica
- revelacion

Nota de diseno:

- el pasillo de piedra no debe sentirse como relleno; prepara el paso de lo ritual a lo hidraulico y material

## Bloqueos y aperturas relevantes

- `4 <-> 6`: acceso frontal cerrado desde fuera hasta abrirlo desde la finca.
- `5 <-> 19`: requiere colocar la tabla suelta sobre la zanja.
- `15 <-> 16`: requiere resolver el mecanismo de la capilla.
- `16 -> 20`: requiere levantar la losa con la vara metalica y contar con luz estable.
- `22 -> 23`: requiere superar el aljibe con cuerda y gancho.
- `23 -> 24`: requiere abrir la gruta sellada usando placa y copa.

## Notas sobre backtracking razonable

- El gran atajo del juego es abrir la zona frontal desde dentro.
- La casa principal funciona como centro de redistribucion antes de anexos.
- La distancia entre la capilla y la sacristia es corta para no castigar ensayo y comprobacion.
- El subsuelo es compacto para que el final no se convierta en una caminata larga.
- Los objetos criticos se obtienen antes de que su uso requiera recorridos excesivos.
