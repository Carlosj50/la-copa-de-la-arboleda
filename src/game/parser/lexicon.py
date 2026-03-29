"""Parser lexicon and normalization tables."""

from __future__ import annotations


SPECIAL_ALIASES: dict[str, str] = {
    "QUE VES": "MIRAR",
    "SALIR JUEGO": "FIN",
}

VERB_ALIASES: dict[str, str] = {
    "MIRAR": "MIRAR",
    "MIRA": "MIRAR",
    "VER": "VER",
    "OBSERVAR": "MIRAR",
    "OBSERVA": "MIRAR",
    "EXAMINAR": "EXAMINAR",
    "EXAMINA": "EXAMINAR",
    "INSPECCIONAR": "EXAMINAR",
    "IR": "IR",
    "AVANZAR": "IR",
    "ENTRAR": "ENTRAR",
    "ENTRA": "ENTRAR",
    "SALIR": "SALIR",
    "COGER": "COGER",
    "COGE": "COGER",
    "TOMAR": "COGER",
    "TOMA": "COGER",
    "RECOGER": "COGER",
    "RECOGE": "COGER",
    "SOLTAR": "SOLTAR",
    "SUELTA": "SOLTAR",
    "DEJAR": "SOLTAR",
    "DEJA": "SOLTAR",
    "ABRIR": "ABRIR",
    "ABRE": "ABRIR",
    "CERRAR": "CERRAR",
    "CIERRA": "CERRAR",
    "USAR": "USAR",
    "USA": "USAR",
    "PONER": "USAR",
    "PON": "USAR",
    "EMPUJAR": "EMPUJAR",
    "EMPUJA": "EMPUJAR",
    "TIRAR": "TIRAR",
    "TIRA": "TIRAR",
    "LEER": "LEER",
    "LEE": "LEER",
    "ENCENDER": "ENCENDER",
    "ENCIENDE": "ENCENDER",
    "APAGAR": "APAGAR",
    "APAGA": "APAGAR",
    "INVENTARIO": "INVENTARIO",
    "INV": "INVENTARIO",
    "I": "INVENTARIO",
    "AYUDA": "AYUDA",
    "GUARDAR": "GUARDAR",
    "GUARDA": "GUARDAR",
    "CARGAR": "CARGAR",
    "CARGA": "CARGAR",
    "FIN": "FIN",
}

DIRECTION_ALIASES: dict[str, str] = {
    "NORTE": "NORTE",
    "N": "NORTE",
    "SUR": "SUR",
    "S": "SUR",
    "ESTE": "ESTE",
    "E": "ESTE",
    "OESTE": "OESTE",
    "O": "OESTE",
    "ARRIBA": "ARRIBA",
    "ABAJO": "ABAJO",
    "IZQUIERDA": "IZQUIERDA",
    "DERECHA": "DERECHA",
}

PREPOSITIONS = {"EN", "CON", "A", "AL"}
STOPWORDS = {"EL", "LA", "LOS", "LAS", "UN", "UNA", "UNOS", "UNAS"}
