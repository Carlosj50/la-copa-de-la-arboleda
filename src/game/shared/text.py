"""Text normalization and formatting helpers."""

from __future__ import annotations

import re
import textwrap
import unicodedata


PUNCTUATION_RE = re.compile(r"[^\w\s]")
SPACES_RE = re.compile(r"\s+")
SCREEN_TEXT_WIDTH = 76


def strip_accents(value: str) -> str:
    """Return an accent-free representation of *value*."""

    normalized = unicodedata.normalize("NFD", value)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_text(value: str) -> str:
    """Normalize player-facing text for command matching."""

    stripped = strip_accents(value).upper()
    without_punctuation = PUNCTUATION_RE.sub(" ", stripped)
    return SPACES_RE.sub(" ", without_punctuation).strip()


def format_series(values: list[str]) -> str:
    """Format a Spanish series with a natural final conjunction."""

    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} y {values[1]}"
    return f"{', '.join(values[:-1])} y {values[-1]}"


def wrap_for_screen(text: str, width: int = SCREEN_TEXT_WIDTH) -> str:
    """Wrap screen text without breaking words."""

    wrapped_lines: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            wrapped_lines.append("")
            continue
        wrapped_lines.extend(
            textwrap.wrap(
                line,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return "\n".join(wrapped_lines)
