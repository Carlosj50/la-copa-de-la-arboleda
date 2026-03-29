# La Copa de la Arboleda

<p align="center">
  Aventura conversacional retro para consola, escrita en Python, con parser controlado, exploración pausada y misterio rural.
</p>

<p align="center">
  <img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white">
  <img alt="Estado jugable" src="https://img.shields.io/badge/estado-jugable-3f8f4b">
  <img alt="Interfaz consola" src="https://img.shields.io/badge/interfaz-consola-1b1b1b">
  <img alt="Windows first" src="https://img.shields.io/badge/plataforma-Windows%20first-0078D4">
</p>

## Capturas

<p align="center">
  <img src="docs/assets/screenshots/01-apertura.svg" alt="Pantalla de apertura" width="48%">
  <img src="docs/assets/screenshots/02-camino-entrada.svg" alt="Camino de entrada" width="48%">
</p>

<p align="center">
  <img src="docs/assets/screenshots/03-capilla-ruinas.svg" alt="Capilla en ruinas" width="48%">
  <img src="docs/assets/screenshots/04-camara-aljibe.svg" alt="Cámara del aljibe" width="48%">
</p>

## Premisa

Tras la muerte de un familiar solitario, el protagonista recibe una carpeta con notas incompletas, un croquis torpe y una frase repetida hasta la obsesión:

> "No la busques en la casa. La copa guarda el camino."

Lo que empieza como la búsqueda de una copa de plata acaba convirtiéndose en una exploración de la finca de La Arboleda, sus anexos olvidados y una zona subterránea sellada durante décadas.

## Ficha rápida

- 24 pantallas / habitaciones
- 4 zonas conectadas
- 9 hitos principales de progreso
- 14 objetos principales de interacción
- 4 hallazgos opcionales con peso real
- 15 elementos fijos interactivos del entorno
- 1 final principal con variante

## Qué ofrece el proyecto

- aventura conversacional original con tono de misterio, melancolía y tensión suave
- motor modular en Python 3.12, sin framework gráfico ni app web
- parser V1 corto, claro y deliberadamente acotado
- 24 habitaciones, 4 zonas y progresión completa definida desde el inicio
- contenido authored en JSON, separado del runtime
- una sola pantalla limpia por interacción, con escenas pixeladas austeras dentro de la consola
- guardado y carga de partida en local

## Filosofía de diseño

La experiencia está pensada para:

- explorar con calma
- observar antes de actuar
- reconstruir el espacio mentalmente
- tomar notas
- dibujar el mapa en papel si apetece

No busca:

- parser de lenguaje libre
- ayudas invasivas
- mapa automático
- motor gráfico
- interfaz moderna tipo visual novel

## Estado actual

El repositorio contiene una versión base jugable de principio a fin con:

- parser, inventario, flags, interacciones y persistencia
- mundo completo cargado desde datos
- finales principal y variante
- pruebas automatizadas con `unittest`
- documentación de diseño y de arquitectura

## Puesta en marcha

### Windows

Crear y activar el entorno virtual:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Ejecutar el juego:

```powershell
python -m game
```

También puedes usar el lanzador:

- `JUGAR_LA_COPA.bat`

Generar un ejecutable de Windows:

```powershell
python -m pip install -e .[build]
.\GENERAR_EXE.bat
```

Salida esperada:

- `dist\LaCopaDeLaArboleda.exe`

### WSL

```bash
cmd.exe /c py -3.12 -m venv G:\\juegopcaventuraconversacional\\.venv
/mnt/g/juegopcaventuraconversacional/.venv/Scripts/python.exe -m pip install -e /mnt/g/juegopcaventuraconversacional
/mnt/g/juegopcaventuraconversacional/.venv/Scripts/python.exe -m game
```

Generar el `.exe` de Windows desde WSL:

```bash
/mnt/g/juegopcaventuraconversacional/.venv/Scripts/python.exe -m pip install -e /mnt/g/juegopcaventuraconversacional[build]
cmd.exe /c G:\\juegopcaventuraconversacional\\GENERAR_EXE.bat
```

## Comandos útiles

- `MIRAR`, `MIRA`, `VER`
- `EXAMINAR OBJETO`
- `NORTE`, `SUR`, `ESTE`, `OESTE`, `ARRIBA`, `ABAJO`
- `COGER`, `COGE`, `RECOGE`
- `USAR OBJETO EN OBJETO`
- `LEER`, `ABRIR`, `EMPUJAR`, `TIRAR`
- `INVENTARIO`, `AYUDA`, `GUARDAR`, `CARGAR`, `FIN`

La ayuda completa para jugar está en:

- `MANUAL_JUGADOR.md`

## Documentación del proyecto

- `MANUAL_JUGADOR.md`: manual breve para jugar
- `STATE.md`: fotografía operativa del repositorio
- `docs/`: especificación de diseño, narrativa y arquitectura
- `docs/RUNBOOK.md`: preparación de entorno, ejecución y reglas de trabajo

## Desarrollo

Ejecutar pruebas:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Regenerar capturas del README:

```bash
python scripts/generate_readme_assets.py
```

Generar el ejecutable de Windows:

```powershell
python -m pip install -e .[build]
.\GENERAR_EXE.bat
```

## Estructura

```text
.
├── data/
│   ├── saves/
│   └── world/
├── docs/
├── scripts/
├── src/
│   └── game/
├── tests/
├── AGENTS.md
├── JUGAR_LA_COPA.bat
├── MANUAL_JUGADOR.md
├── README.md
└── STATE.md
```

## Principios técnicos

- Python simple antes que complejidad gratuita
- biblioteca estándar primero
- dependencia externa de build solo cuando aporta una salida clara, como el `.exe` de Windows
- contenido separado del motor
- cambios pequeños y trazables
- arquitectura mantenible antes que "brillante"

## Nota sobre las capturas

Las capturas del README se generan desde el propio runtime del juego y se exportan como SVG para que puedan versionarse y mantenerse dentro del repositorio.
