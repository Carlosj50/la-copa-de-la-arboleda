# STATE

Fecha de referencia: 29-03-2026

## Naturaleza del archivo

`STATE.md` es una fotografia operativa del repositorio. No redefine la especificacion: la spec vive en `docs/`.

## Estado actual

Repositorio con build jugable, corpus documental coherente y cierre funcional suficiente para considerarlo una `v0.1.0`.

## Ya decidido

- aventura conversacional retro para consola
- Python 3.12 como lenguaje objetivo
- Windows como plataforma inicial
- entorno virtual local en `.venv`
- parser V1 limitado y controlado
- mundo completo disenado desde el inicio
- contenido separado del motor y del parser
- persistencia local simple en JSON
- preferencia por biblioteca estandar

## Ajustes cerrados en esta pasada

- separacion aclarada entre especificacion, estado operativo y datos del mundo
- `fixture` formalizado como tipo de objeto authored
- esquema JSON acotado a un conjunto cerrado de condiciones y efectos soportados
- progresion reclasificada como `9 hitos principales` en vez de inflar todos como puzles mecanicos
- correccion de aliases de habitaciones que pisaban fixtures locales
- validacion de contenido reforzada para detectar referencias rotas y colisiones locales
- pistas narrativas afinadas para que la casa guarde claves, no una falsa solucion
- pulido inicial de textos en la apertura, tramo domestico y pasillo final
- pulido selectivo de tono en biblioteca, dormitorio, capilla, aljibe y camara final
- persistencia endurecida frente a saves incompletos o corruptos
- cobertura automatica ampliada para parser, contenido, persistencia y flujo contextual

## Entregado

- base documental completa y corregida
- paquete Python instalable
- parser V1 funcional
- mundo completo de 24 habitaciones cargado desde JSON
- motor de consola jugable de principio a fin
- escenas pixeladas austeras para la portada y varias habitaciones iniciales
- compositor de pantalla fija con marco retro, bloque de escena y bloque de resultado
- compositor afinado con color tenue, subtitulo de zona y pie util de comandos
- repintado completo de consola para que cada interaccion ocupe una sola pantalla
- ancho fijo de composicion para evitar cortes feos de texto en pantalla
- rosa de los vientos fija en la esquina superior derecha como ayuda visual no invasiva
- escenas ampliadas con respaldos por zona y una cobertura mas amplia de salas interiores, anexos y tramo final
- arranque de Windows afinado para UTF-8 real en consola
- manual breve de jugador en raiz para orientar la experiencia sin invadir la interfaz
- guardado y carga en JSON
- finales principal y variante
- 46 pruebas automatizadas base y de regresion
- build reproducible de `LaCopaDeLaArboleda.exe` para Windows con PyInstaller

## Pendiente

- pulido fino del resto de textos y respuestas secundarios
- decidir si se quiere ampliar todavia mas la cobertura de escenas a otras habitaciones
- pasada manual de ritmo y justicia de puzles
- validacion mas estricta de aliases globales si el contenido crece
- decidir si se quiere una herramienta auxiliar de autoria mas adelante
- decidir si en una futura release se quiere adjuntar el `.exe` como asset descargable

## Riesgos residuales

- que `docs/` y `data/world` vuelvan a divergir si se editan por separado
- crecimiento del lexico del parser sin pruebas de regresion
- acumulacion de excepciones de contenido si se amplian puzles sin mantener el conjunto cerrado de handlers
- abuso futuro de aliases genericos que reabra ambiguedades de parser
- exceso de escenas si se intenta ilustrar todo el mapa sin criterio atmosferico
- tentacion de reintroducir ayudas visuales persistentes que resten valor al mapeado en papel

## Proximo paso recomendado

Siguiente foco razonable:

- pulido narrativo y de respuestas
- ampliacion de pruebas del parser y del flujo opcional
- revision manual completa del ritmo de apertura y del backtracking medio
- decidir si tras `v0.1.0` se quiere abrir una fase de herramientas de autor o mantener solo pulido incremental
