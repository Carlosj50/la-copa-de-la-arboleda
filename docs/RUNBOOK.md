# Runbook

Ultima actualizacion: 29-03-2026

## Preparar entorno

### Windows PowerShell

Crear entorno virtual:

```powershell
py -3.12 -m venv .venv
```

Activarlo:

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

Crear entorno virtual:

```bat
py -3.12 -m venv .venv
```

Activarlo:

```bat
.venv\Scripts\activate.bat
```

### WSL sobre el proyecto en `G:\`

Si se necesita crear el entorno de Windows desde WSL:

```bash
cmd.exe /c py -3.12 -m venv G:\\juegopcaventuraconversacional\\.venv
```

## Instalar dependencias

No hay dependencias runtime externas aprobadas para V1.

Instalacion recomendada:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

## Ejecutar el proyecto

Comando:

```bash
python -m game
```

Documento recomendado para jugar:

- `MANUAL_JUGADOR.md`

Opciones de presentacion disponibles por entorno:

```bash
LA_COPA_VISUAL=0 python -m game
LA_COPA_COMPACT=1 python -m game
LA_COPA_SCREEN_WIDTH=92 LA_COPA_TEXT_WIDTH=76 python -m game
```

En Windows CMD se pueden fijar antes de arrancar:

```bat
set LA_COPA_VISUAL=0
set LA_COPA_COMPACT=1
python -m game
```

## Ejecutar pruebas

Estrategia prevista con stdlib:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Si se aprueba otra herramienta en el futuro, la decision debe quedar documentada antes.

## Anadir contenido nuevo

Flujo recomendado:

1. revisar `docs/WORLD_BIBLE.md`, `docs/ROOM_INDEX.md`, `docs/OBJECT_CATALOG.md` y `docs/PUZZLE_FLOW.md`
2. revisar tambien `docs/WORLD_MODEL.md` y `docs/DATA_FORMAT.md` si toca schema o comportamiento
3. actualizar la especificacion si el cambio altera el diseno
4. modificar los JSON de `data/world`
5. ajustar validadores o handlers necesarios
6. anadir o actualizar pruebas
7. reflejar el cambio en `STATE.md` si cambia el alcance o el estado real del proyecto

## Guardado de partidas

Ruta prevista:

- `data/saves/`

Convencion inicial sugerida:

- `slot_001.json`
- `slot_002.json`

## Regla de disciplina operativa

Antes de tocar arquitectura, parser o formato de datos:

- leer especificaciones relevantes
- decidir si el cambio es local o estructural
- documentar primero si es estructural
- ejecutar validaciones y pruebas despues del cambio
