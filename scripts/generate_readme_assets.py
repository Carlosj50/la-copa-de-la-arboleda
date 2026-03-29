"""Generate README screenshots from the current terminal UI."""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from game.content import load_game_definition
from game.engine import GameSession
from game.persistence import SaveSystem
from game.shared.screen import visible_width


ANSI_RE = re.compile(r"\x1b\[([0-9;]*)m")
DEFAULT_FG = "#d9d7d0"
BG = "#0c0c0f"
PANEL = "#111216"
PANEL_EDGE = "#2b2d33"
TITLEBAR = "#17181c"
ACCENT = "#c7ae7a"
FONT_FAMILY = "Consolas, 'Cascadia Mono', 'Courier New', monospace"
FONT_SIZE = 18
LINE_HEIGHT = 24
CHAR_WIDTH = 10.8
PADDING_X = 34
PADDING_Y = 26
TITLEBAR_HEIGHT = 42
SCREEN_DIR = PROJECT_ROOT / "docs" / "assets" / "screenshots"


@dataclass
class TextStyle:
    fg: str = DEFAULT_FG
    bold: bool = False


@dataclass
class Segment:
    text: str
    style: TextStyle


def parse_ansi_line(line: str) -> list[Segment]:
    segments: list[Segment] = []
    style = TextStyle()
    cursor = 0
    for match in ANSI_RE.finditer(line):
        chunk = line[cursor:match.start()]
        if chunk:
            segments.append(Segment(chunk, TextStyle(style.fg, style.bold)))
        style = apply_sgr(match.group(1), style)
        cursor = match.end()

    tail = line[cursor:]
    if tail:
        segments.append(Segment(tail, TextStyle(style.fg, style.bold)))
    return segments


def apply_sgr(raw_codes: str, current: TextStyle) -> TextStyle:
    if not raw_codes:
        return TextStyle()

    codes = [code for code in raw_codes.split(";") if code]
    if not codes:
        return TextStyle()

    style = TextStyle(current.fg, current.bold)
    index = 0
    while index < len(codes):
        code = codes[index]
        if code == "0":
            style = TextStyle()
        elif code == "1":
            style.bold = True
        elif code == "22":
            style.bold = False
        elif code == "39":
            style.fg = DEFAULT_FG
        elif code == "38" and index + 4 < len(codes) and codes[index + 1] == "2":
            red = int(codes[index + 2])
            green = int(codes[index + 3])
            blue = int(codes[index + 4])
            style.fg = f"#{red:02x}{green:02x}{blue:02x}"
            index += 4
        index += 1
    return style


def svg_escape(value: str) -> str:
    return html.escape(value).replace(" ", "&#160;")


def render_screen_svg(title: str, screen_text: str, output_path: Path) -> None:
    lines = screen_text.splitlines()
    visible_max = max((visible_width(line) for line in lines), default=0)
    width = int((visible_max * CHAR_WIDTH) + (PADDING_X * 2))
    height = int((len(lines) * LINE_HEIGHT) + (PADDING_Y * 2) + TITLEBAR_HEIGHT)

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "  <defs>",
        '    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>',
        "    </filter>",
        "  </defs>",
        f'  <rect width="{width}" height="{height}" rx="20" fill="{BG}"/>',
        f'  <g filter="url(#shadow)">',
        f'    <rect x="16" y="16" width="{width - 32}" height="{height - 32}" rx="16" fill="{PANEL}" stroke="{PANEL_EDGE}" />',
        f'    <rect x="16" y="16" width="{width - 32}" height="{TITLEBAR_HEIGHT}" rx="16" fill="{TITLEBAR}" />',
        f'    <rect x="16" y="{16 + TITLEBAR_HEIGHT - 16}" width="{width - 32}" height="16" fill="{TITLEBAR}" />',
        '    <circle cx="42" cy="37" r="6" fill="#ff5f57"/>',
        '    <circle cx="62" cy="37" r="6" fill="#febc2e"/>',
        '    <circle cx="82" cy="37" r="6" fill="#28c840"/>',
        (
            f'    <text x="{width / 2:.1f}" y="42" fill="{ACCENT}" '
            f'font-family="{FONT_FAMILY}" font-size="16" font-weight="700" text-anchor="middle">'
            f"{html.escape(title)}</text>"
        ),
        "  </g>",
    ]

    y = 16 + TITLEBAR_HEIGHT + PADDING_Y
    x = 16 + PADDING_X
    for line in lines:
        segments = parse_ansi_line(line)
        if not segments:
            segments = [Segment(" ", TextStyle())]
        svg_lines.append(
            f'  <text x="{x}" y="{y}" fill="{DEFAULT_FG}" font-family="{FONT_FAMILY}" '
            f'font-size="{FONT_SIZE}" xml:space="preserve">'
        )
        for segment in segments:
            weight = "700" if segment.style.bold else "400"
            svg_lines.append(
                f'    <tspan fill="{segment.style.fg}" font-weight="{weight}">{svg_escape(segment.text)}</tspan>'
            )
        svg_lines.append("  </text>")
        y += LINE_HEIGHT

    svg_lines.append("</svg>")
    output_path.write_text("\n".join(svg_lines), encoding="utf-8")


def build_session() -> GameSession:
    definition = load_game_definition(PROJECT_ROOT / "data" / "world")
    save_system = SaveSystem(PROJECT_ROOT / "data" / "saves" / "_readme_assets.json")
    return GameSession(definition, save_system)


def build_screens() -> dict[str, str]:
    opening = build_session()
    opening.screen.options.show_scene

    exterior = build_session()

    capilla = build_session()
    capilla.state.current_room_id = "capilla_ruinas"

    aljibe = build_session()
    aljibe.state.current_room_id = "camara_aljibe"

    return {
        "01-apertura.svg": opening.opening_text(),
        "02-camino-entrada.svg": exterior.render_room_screen(force_full=True),
        "03-capilla-ruinas.svg": capilla.render_room_screen(force_full=True),
        "04-camara-aljibe.svg": aljibe.render_room_screen(force_full=True),
    }


def main() -> int:
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    screens = build_screens()
    for filename, content in screens.items():
        render_screen_svg("La Copa de la Arboleda", content, SCREEN_DIR / filename)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
