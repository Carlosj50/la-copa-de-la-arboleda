# Object Catalog

Ultima actualizacion: 29-03-2026

## Regla general

El catalogo distingue cuatro clases:

- `main`: objeto principal de progreso
- `optional`: pista o hallazgo opcional con peso real
- `fixture`: elemento fijo del entorno con el que se puede interactuar
- `ambient`: detalle atmosferico sin funcion mecanica principal

Regla de alias:

- un alias de habitacion no debe pisar un objeto o fixture local
- un alias generico no debe darse a un ambiental si puede chocar con un objeto critico

## Objetos interactivos principales

### 1. Copa de plata

- Tipo: `main`, obligatoria
- Donde aparece: 15, tras resolver la capilla
- Utilidad: llave simbolica y practica del tramo final
- Interacciones esperadas: coger, examinar, usar con agua, devolver al pedestal

### 2. Cuaderno del familiar

- Tipo: `main`, obligatorio
- Donde aparece: 13
- Utilidad: orientar la lectura correcta del lugar
- Interacciones esperadas: coger, leer, examinar

### 3. Llave oxidada

- Tipo: `main`, obligatoria
- Donde aparece: 10
- Utilidad: abrir el cuarto de aperos
- Interacciones esperadas: coger, examinar, usar en puerta de aperos

### 4. Caja de cerillas

- Tipo: `main`, obligatoria
- Donde aparece: 10
- Utilidad: encender la lampara
- Interacciones esperadas: coger, examinar

### 5. Lampara de aceite

- Tipo: `main`, obligatoria
- Donde aparece: 13
- Utilidad: luz estable para el subsuelo
- Interacciones esperadas: coger, examinar, encender, apagar

### 6. Botella de aceite

- Tipo: `main`, obligatoria
- Donde aparece: 18
- Utilidad: rellenar la lampara
- Interacciones esperadas: coger, examinar, usar con la lampara

### 7. Cuerda

- Tipo: `main`, obligatoria
- Donde aparece: 14
- Utilidad: resolver el paso del aljibe
- Interacciones esperadas: coger, examinar, usar con anillas

### 8. Pala pequena

- Tipo: `main`, obligatoria
- Donde aparece: 14
- Utilidad: desenterrar el medallon
- Interacciones esperadas: coger, examinar, usar en bancal

### 9. Medallon con simbolo

- Tipo: `main`, obligatorio
- Donde aparece: 18, oculto en el bancal
- Utilidad: activar el mecanismo de la capilla
- Interacciones esperadas: coger, examinar, usar en altar

### 10. Vara metalica

- Tipo: `main`, obligatoria
- Donde aparece: 17
- Utilidad: hacer palanca en la losa
- Interacciones esperadas: coger, examinar, usar en losa

### 11. Trozo de vidriera

- Tipo: `main`, obligatorio
- Donde aparece: 12
- Utilidad: completar el roseton
- Interacciones esperadas: coger, examinar, usar en roseton

### 12. Tabla suelta

- Tipo: `main`, obligatoria
- Donde aparece: 3
- Utilidad: salvar la zanja de la valla
- Interacciones esperadas: coger, examinar, usar en zanja
- Nota: tras fijarse, deja de ser portable

### 13. Gancho de hierro

- Tipo: `main`, obligatorio
- Donde aparece: 14
- Utilidad: completar la solucion del aljibe junto con la cuerda
- Interacciones esperadas: coger, examinar, usar con anillas

### 14. Placa de piedra grabada

- Tipo: `main`, obligatoria
- Donde aparece: 16
- Utilidad: abrir la gruta sellada e interpretar el gesto final
- Interacciones esperadas: coger, leer, examinar, usar en hendidura

## Hallazgos opcionales con peso real

### Retrato danado

- Tipo: `optional`
- Donde aparece: 7
- Funcion: activa una pista de comprension sobre Adela y el simbolo del arbol con copa

### Nota encerada

- Tipo: `optional`
- Donde aparece: 11, oculta en el falso fondo
- Funcion: suaviza la busqueda del aceite y del aljibe

### Legajos de la finca

- Tipo: `optional`
- Donde aparece: 12
- Funcion: anade contexto historico sobre Adela e Inocencio

### Carta de Salvador

- Tipo: `optional`
- Donde aparece: 13, oculta en el cajon
- Funcion: refuerza el final variante y la eleccion del protagonista

## Fixtures interactivos

### Pozo seco

- Sala: 3
- Funcion: fija tono y focaliza la exploracion del claro

### Verja frontal

- Sala: 4
- Funcion: anuncia el atajo frontal y su apertura futura desde dentro

### Zanja

- Sala: 5
- Funcion: bloqueo fisico del acceso lateral

### Puerta de aperos

- Sala: 6
- Funcion: bloqueo de herramientas

### Falso fondo

- Sala: 11
- Funcion: soporte del desvio opcional de despensa

### Cajon oculto

- Sala: 13
- Funcion: soporte del desvio opcional del dormitorio

### Roseton

- Sala: 15
- Funcion: mitad visible del mecanismo de capilla

### Altar

- Sala: 15
- Funcion: segunda mitad del mecanismo de capilla

### Losa del subterraneo

- Sala: 16
- Funcion: cierre fisico del descenso

### Bancal frio

- Sala: 18
- Funcion: escondite del medallon

### Anillas del aljibe

- Sala: 22
- Funcion: soporte material del paso asegurado

### Agua del aljibe

- Sala: 22
- Funcion: llena la copa para el gesto final

### Hendidura

- Sala: 23
- Funcion: recibe la placa grabada

### Cuenco de piedra

- Sala: 23
- Funcion: recibe el agua de la copa

### Pedestal final

- Sala: 24
- Funcion: recibe la copa y abre el archivo

## Objetos ambientales

### Cuchara vieja

- Sala: 9
- Funcion: reforzar costumbre rota y vida domestica suspendida

### Copa rota

- Sala: 8
- Funcion: eco falso de la copa verdadera sin reclamar el alias principal `copa`

### Reloj parado

- Sala: 8
- Funcion: subrayar la detencion del tiempo

### Rosario

- Sala: 15
- Funcion: cargar de tono la capilla sin convertirlo en un puzzle

### Libro humedo

- Sala: 12
- Funcion: reforzar decadencia material de la biblioteca

### Cajon roto

- Sala: 10
- Funcion: reforzar uso practico continuado de la cocina

### Herramienta sin mango

- Sala: 14
- Funcion: tono practico y desgaste del cuarto de aperos

### Cubos viejos

- Sala: 3 y 17
- Funcion: continuidad material del abandono

### Ramas secas

- Sala: 1 y 18
- Funcion: continuidad tonal entre exterior e interior degradado
