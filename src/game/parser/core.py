"""Command parser."""

from __future__ import annotations

from game.model import ParsedCommand
from game.shared.text import normalize_text

from .lexicon import DIRECTION_ALIASES, PREPOSITIONS, SPECIAL_ALIASES, STOPWORDS, VERB_ALIASES


def _compact_object_tokens(tokens: list[str]) -> str | None:
    filtered = [token for token in tokens if token not in STOPWORDS]
    if not filtered:
        return None
    return " ".join(filtered)


def parse_command(raw_text: str) -> ParsedCommand:
    """Parse a raw player command into a structured command."""

    normalized = normalize_text(raw_text)
    if not normalized:
        return ParsedCommand(action="ERROR", raw_text=raw_text, error_message="No has escrito ningún comando.")

    if normalized in SPECIAL_ALIASES:
        normalized = SPECIAL_ALIASES[normalized]

    tokens = normalized.split()
    if len(tokens) == 2:
        combined = " ".join(tokens)
        if combined in SPECIAL_ALIASES:
            normalized = SPECIAL_ALIASES[combined]
            tokens = normalized.split()

    if len(tokens) == 1 and tokens[0] in DIRECTION_ALIASES:
        return ParsedCommand(action="IR", raw_text=raw_text, direction=DIRECTION_ALIASES[tokens[0]])

    first = tokens[0]
    action = VERB_ALIASES.get(first)
    if action is None:
        return ParsedCommand(action="ERROR", raw_text=raw_text, error_message="No entiendo ese verbo.")

    if action == "VER":
        action = "MIRAR" if len(tokens) == 1 else "EXAMINAR"

    if action == "FIN":
        return ParsedCommand(action="FIN", raw_text=raw_text)

    if len(tokens) == 1:
        return ParsedCommand(action=action, raw_text=raw_text)

    if action == "IR":
        direction = DIRECTION_ALIASES.get(tokens[1])
        if direction is None:
            return ParsedCommand(
                action="ERROR",
                raw_text=raw_text,
                error_message="Ese formato no está soportado en esta versión.",
            )
        return ParsedCommand(action="IR", raw_text=raw_text, direction=direction)

    if action in {"ENTRAR", "SALIR"} and len(tokens) == 1:
        return ParsedCommand(action=action, raw_text=raw_text)

    if action in {"MIRAR", "EXAMINAR"}:
        direct_text = _compact_object_tokens(tokens[1:])
        if direct_text is None:
            return ParsedCommand(action="MIRAR", raw_text=raw_text)
        return ParsedCommand(action="EXAMINAR", raw_text=raw_text, direct_text=direct_text)

    preposition_index = None
    preposition_value = None
    for index, token in enumerate(tokens[1:], start=1):
        if token in PREPOSITIONS:
            preposition_index = index
            preposition_value = "A" if token == "AL" else token
            break

    if preposition_index is None:
        direct_text = _compact_object_tokens(tokens[1:])
        if direct_text is None:
            return ParsedCommand(
                action="ERROR",
                raw_text=raw_text,
                error_message="Te falta concretar la acción.",
            )
        return ParsedCommand(action=action, raw_text=raw_text, direct_text=direct_text)

    direct_text = _compact_object_tokens(tokens[1:preposition_index])
    indirect_text = _compact_object_tokens(tokens[preposition_index + 1 :])
    if direct_text is None or indirect_text is None:
        return ParsedCommand(
            action="ERROR",
            raw_text=raw_text,
            error_message="Ese formato no está soportado en esta versión.",
        )

    return ParsedCommand(
        action=action,
        raw_text=raw_text,
        direct_text=direct_text,
        indirect_text=indirect_text,
        preposition=preposition_value,
    )
