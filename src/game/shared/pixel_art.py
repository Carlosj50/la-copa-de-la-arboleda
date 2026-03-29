"""Minimal static pixel scenes for the console."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache


RESET = "\x1b[0m"
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
STD_OUTPUT_HANDLE = -11

PALETTE: dict[str, tuple[int, int, int]] = {
    "night": (16, 18, 24),
    "mist": (76, 86, 92),
    "leaf": (45, 73, 52),
    "leaf_light": (72, 108, 72),
    "vine": (58, 92, 56),
    "bark": (97, 72, 52),
    "path": (146, 124, 92),
    "stone": (158, 160, 160),
    "stone_dark": (88, 92, 96),
    "gate": (90, 92, 96),
    "house": (108, 112, 116),
    "house_dark": (60, 64, 70),
    "window": (192, 162, 92),
    "wall": (104, 96, 86),
    "floor": (92, 68, 48),
    "soil": (86, 58, 38),
    "frame": (132, 86, 46),
    "portrait": (186, 174, 134),
    "folder": (167, 139, 83),
    "folder_light": (197, 169, 109),
    "paper": (228, 220, 188),
    "desk": (61, 47, 35),
    "ink": (44, 36, 28),
    "water": (58, 88, 112),
    "water_light": (96, 132, 156),
    "copper": (166, 114, 70),
    "amber": (214, 178, 106),
}


@dataclass
class PixelCell:
    """A single rendered cell."""

    bg: str | None = None
    glyph: str = " "
    fg: str | None = None


class PixelCanvas:
    """Small mutable canvas used to author room scenes with code."""

    def __init__(self, width: int, height: int, bg: str | None = None) -> None:
        self.width = width
        self.height = height
        self._cells = [
            [PixelCell(bg=bg) for _ in range(width)]
            for _ in range(height)
        ]

    def fill_rect(self, x: int, y: int, width: int, height: int, color: str) -> None:
        for row in range(y, y + height):
            for column in range(x, x + width):
                self.paint(column, row, color)

    def draw_rect(self, x: int, y: int, width: int, height: int, color: str) -> None:
        for column in range(x, x + width):
            self.paint(column, y, color)
            self.paint(column, y + height - 1, color)
        for row in range(y, y + height):
            self.paint(x, row, color)
            self.paint(x + width - 1, row, color)

    def fill_span(self, y: int, x_start: int, x_end: int, color: str) -> None:
        for column in range(x_start, x_end + 1):
            self.paint(column, y, color)

    def paint(self, x: int, y: int, color: str) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self._cells[y][x]
            cell.bg = color
            if cell.glyph == " ":
                cell.fg = None

    def put_text(
        self,
        x: int,
        y: int,
        text: str,
        fg: str,
        bg: str | None = None,
    ) -> None:
        for index, glyph in enumerate(text):
            column = x + index
            if 0 <= column < self.width and 0 <= y < self.height:
                self._cells[y][column] = PixelCell(bg=bg, glyph=glyph, fg=fg)

    def render(self) -> str:
        lines: list[str] = []
        for row in self._cells:
            parts: list[str] = []
            for cell in row:
                if cell.glyph != " ":
                    parts.append(_styled_glyph(cell.glyph, cell.fg, cell.bg))
                elif cell.bg:
                    parts.append(_styled_glyph("█", cell.bg, None))
                else:
                    parts.append(" ")
            lines.append("".join(parts).rstrip())
        return "\n".join(lines)


def enable_console_ansi() -> None:
    """Best-effort ANSI support for Windows terminals."""

    if os.name != "nt" or not sys.stdout.isatty():
        return

    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        mode = ctypes.c_uint()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(
                handle,
                mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING,
            )
    except Exception:
        return


def has_scene(scene_id: str | None) -> bool:
    """Return True if *scene_id* is empty or known."""

    return scene_id is None or scene_id in _SCENE_BUILDERS


@lru_cache(maxsize=None)
def render_scene(scene_id: str | None) -> str:
    """Render a known static scene."""

    if scene_id is None:
        return ""
    builder = _SCENE_BUILDERS.get(scene_id)
    if builder is None:
        raise ValueError(f"Unknown scene: {scene_id}")
    return builder().render()


def _styled_glyph(glyph: str, fg_color: str | None, bg_color: str | None) -> str:
    codes: list[str] = []
    if fg_color:
        red, green, blue = PALETTE[fg_color]
        codes.append(f"38;2;{red};{green};{blue}")
    if bg_color:
        red, green, blue = PALETTE[bg_color]
        codes.append(f"48;2;{red};{green};{blue}")
    if not codes:
        return glyph
    return f"\x1b[{';'.join(codes)}m{glyph}{RESET}"


def _draw_tree(canvas: PixelCanvas, x: int, trunk_top: int) -> None:
    canvas.fill_rect(x, trunk_top + 2, 1, 4, "bark")
    canvas.fill_rect(x - 1, trunk_top + 1, 3, 2, "leaf")
    canvas.fill_rect(x - 2, trunk_top, 5, 2, "leaf_light")


def _draw_shelf(canvas: PixelCanvas, x: int, y: int, height: int) -> None:
    canvas.fill_rect(x, y, 4, height, "desk")
    for row in range(y + 1, y + height, 3):
        canvas.fill_rect(x, row, 4, 1, "ink")
    for column in range(x + 1, x + 4):
        canvas.paint(column, y + 1, "paper")


def _draw_pedestal(canvas: PixelCanvas, x: int, y: int) -> None:
    canvas.fill_rect(x + 1, y, 3, 1, "stone")
    canvas.fill_rect(x, y + 1, 5, 2, "stone_dark")
    canvas.fill_rect(x + 1, y + 3, 3, 2, "stone")


def _draw_door(canvas: PixelCanvas, x: int, y: int, width: int = 5, height: int = 5) -> None:
    canvas.fill_rect(x, y, width, height, "house_dark")
    canvas.paint(x + width - 2, y + (height // 2), "copper")


def _build_intro_folder() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "night")
    canvas.fill_rect(0, 9, 34, 3, "desk")
    canvas.fill_rect(6, 3, 10, 2, "folder_light")
    canvas.fill_rect(4, 4, 26, 6, "folder")
    canvas.draw_rect(4, 4, 26, 6, "ink")
    canvas.fill_rect(12, 6, 10, 2, "paper")
    canvas.put_text(14, 7, "NOTAS", "ink", "paper")
    canvas.put_text(8, 2, "SALVADOR", "paper", "night")
    canvas.paint(27, 5, "paper")
    canvas.paint(28, 5, "paper")
    canvas.paint(27, 6, "paper")
    canvas.paint(28, 6, "paper")
    return canvas


def _build_camino_entrada() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    for x in range(34):
        if x < 7 or x > 26:
            canvas.paint(x, 0, "leaf")
    _draw_tree(canvas, 3, 1)
    _draw_tree(canvas, 7, 2)
    _draw_tree(canvas, 26, 1)
    _draw_tree(canvas, 30, 2)
    for y in range(3, 12):
        half = max(1, y - 2)
        canvas.fill_span(y, 17 - half, 17 + half, "path")
    for x in (15, 17, 19):
        canvas.paint(x, 2, "house")
    canvas.paint(17, 1, "house_dark")
    for x, y in ((15, 7), (18, 8), (16, 10), (20, 9)):
        canvas.paint(x, y, "stone")
    return canvas


def _build_cruce_bosque() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    _draw_tree(canvas, 4, 1)
    _draw_tree(canvas, 8, 2)
    _draw_tree(canvas, 25, 1)
    _draw_tree(canvas, 29, 2)
    for y in range(7, 12):
        half = 3 + (y - 7)
        canvas.fill_span(y, 17 - half, 17 + half, "path")
    canvas.fill_span(6, 15, 19, "path")
    canvas.fill_span(5, 13, 16, "path")
    canvas.fill_span(4, 10, 13, "path")
    canvas.fill_span(3, 7, 10, "path")
    canvas.fill_span(5, 18, 21, "path")
    canvas.fill_span(4, 21, 24, "path")
    canvas.fill_span(3, 24, 27, "path")
    return canvas


def _build_sendero_piedras() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    canvas.fill_rect(11, 1, 12, 3, "house_dark")
    canvas.fill_rect(12, 2, 10, 2, "house")
    for column in range(13, 22, 2):
        canvas.fill_rect(column, 4, 1, 3, "gate")
    canvas.fill_span(7, 12, 22, "path")
    canvas.fill_span(8, 10, 24, "path")
    canvas.fill_span(9, 9, 25, "path")
    canvas.fill_span(10, 8, 26, "path")
    canvas.fill_span(11, 7, 27, "path")
    for x, y in ((12, 8), (15, 9), (18, 10), (21, 9), (24, 10)):
        canvas.paint(x, y, "stone")
    canvas.fill_rect(0, 4, 6, 8, "leaf")
    canvas.fill_rect(28, 4, 6, 8, "leaf")
    return canvas


def _build_patio_exterior() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    canvas.fill_rect(7, 1, 20, 6, "wall")
    canvas.fill_rect(7, 1, 20, 1, "house_dark")
    canvas.fill_rect(15, 3, 4, 4, "house_dark")
    canvas.fill_rect(10, 4, 3, 3, "window")
    canvas.fill_rect(22, 4, 3, 3, "house_dark")
    canvas.fill_rect(0, 7, 34, 5, "path")
    for x, y in ((9, 9), (13, 8), (19, 10), (23, 9), (27, 10)):
        canvas.paint(x, y, "stone")
    return canvas


def _build_vestibulo() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(13, 2, 8, 4, "frame")
    canvas.fill_rect(14, 3, 6, 2, "portrait")
    canvas.fill_rect(4, 4, 5, 4, "house_dark")
    canvas.fill_rect(26, 4, 5, 4, "house_dark")
    canvas.put_text(15, 4, "I", "ink", "portrait")
    for x in range(1, 34, 2):
        canvas.paint(x, 9, "house_dark")
    return canvas


def _build_exterior_generico() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    _draw_tree(canvas, 4, 1)
    _draw_tree(canvas, 8, 2)
    _draw_tree(canvas, 25, 1)
    _draw_tree(canvas, 29, 2)
    for y in range(5, 12):
        half = 2 + (y - 5)
        canvas.fill_span(y, 17 - half, 17 + half, "path")
    canvas.fill_rect(12, 1, 10, 2, "house_dark")
    return canvas


def _build_interior_generico() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(4, 3, 8, 4, "desk")
    canvas.fill_rect(22, 2, 8, 5, "frame")
    canvas.fill_rect(23, 3, 6, 3, "portrait")
    canvas.fill_rect(14, 5, 6, 2, "house_dark")
    for x in range(2, 34, 3):
        canvas.paint(x, 9, "house_dark")
    return canvas


def _build_anexo_generico() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    canvas.fill_rect(0, 8, 34, 4, "soil")
    canvas.fill_rect(4, 3, 10, 5, "house_dark")
    canvas.fill_rect(5, 4, 8, 3, "wall")
    canvas.fill_rect(20, 2, 10, 6, "leaf")
    canvas.fill_rect(22, 3, 6, 4, "leaf_light")
    for x, y in ((7, 9), (12, 10), (17, 9), (24, 10), (29, 9)):
        canvas.paint(x, y, "stone")
    return canvas


def _build_subterraneo_generico() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 9, 34, 3, "floor")
    canvas.fill_rect(14, 2, 6, 7, "night")
    canvas.fill_rect(13, 3, 8, 5, "night")
    canvas.fill_rect(6, 6, 6, 2, "water")
    canvas.fill_rect(22, 6, 6, 2, "water")
    for x in range(2, 34, 4):
        canvas.paint(x, 10, "stone")
    return canvas


def _build_biblioteca() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    _draw_shelf(canvas, 2, 2, 6)
    _draw_shelf(canvas, 28, 2, 6)
    canvas.fill_rect(12, 5, 10, 2, "desk")
    canvas.fill_rect(15, 4, 4, 1, "paper")
    canvas.paint(19, 4, "window")
    return canvas


def _build_dormitorio() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(3, 4, 11, 3, "desk")
    canvas.fill_rect(4, 3, 9, 3, "paper")
    canvas.fill_rect(21, 3, 8, 4, "house_dark")
    canvas.fill_rect(22, 4, 6, 2, "window")
    canvas.paint(25, 2, "amber")
    canvas.paint(26, 2, "copper")
    return canvas


def _build_salon_principal() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(14, 2, 6, 5, "frame")
    canvas.fill_rect(15, 3, 4, 3, "portrait")
    canvas.fill_rect(4, 4, 7, 3, "desk")
    canvas.fill_rect(24, 4, 5, 3, "desk")
    canvas.put_text(7, 4, "O", "amber", "desk")
    canvas.put_text(25, 6, "x", "paper", "desk")
    for x in range(2, 34, 3):
        canvas.paint(x, 9, "house_dark")
    return canvas


def _build_comedor() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(7, 4, 20, 3, "desk")
    for x in range(9, 27, 4):
        canvas.fill_rect(x, 3, 2, 1, "desk")
        canvas.fill_rect(x, 7, 2, 1, "desk")
    canvas.put_text(24, 5, "/", "paper", "desk")
    return canvas


def _build_cocina() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(4, 4, 11, 3, "desk")
    canvas.fill_rect(19, 3, 9, 4, "stone_dark")
    canvas.fill_rect(20, 4, 7, 2, "stone")
    canvas.fill_rect(7, 3, 3, 1, "paper")
    canvas.put_text(10, 6, "_", "copper", "desk")
    return canvas


def _build_cuarto_aperos() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(4, 2, 26, 1, "desk")
    for x in (7, 11, 16, 22, 27):
        canvas.fill_rect(x, 3, 1, 4, "copper")
    canvas.fill_rect(10, 8, 13, 1, "desk")
    canvas.fill_rect(12, 6, 2, 2, "stone")
    canvas.fill_rect(18, 6, 2, 2, "stone")
    return canvas


def _build_capilla_ruinas() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(13, 2, 8, 5, "wall")
    canvas.fill_rect(14, 3, 6, 3, "stone")
    canvas.paint(17, 4, "window")
    canvas.paint(17, 3, "window")
    canvas.fill_rect(14, 7, 6, 1, "stone")
    canvas.fill_rect(15, 8, 4, 2, "stone_dark")
    canvas.fill_rect(2, 1, 4, 3, "vine")
    canvas.fill_rect(28, 1, 4, 3, "vine")
    return canvas


def _build_sacristia() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    canvas.fill_rect(11, 6, 12, 3, "stone")
    canvas.draw_rect(11, 6, 12, 3, "stone_dark")
    canvas.fill_rect(25, 4, 5, 4, "stone_dark")
    canvas.fill_rect(26, 5, 3, 2, "stone")
    return canvas


def _build_cobertizo() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "wall")
    canvas.fill_rect(0, 8, 34, 4, "floor")
    for x in range(3, 31, 4):
        canvas.fill_rect(x, 2, 1, 6, "desk")
    canvas.fill_rect(6, 3, 7, 4, "house_dark")
    canvas.fill_rect(22, 4, 7, 1, "copper")
    canvas.fill_rect(26, 5, 1, 3, "stone")
    return canvas


def _build_invernadero() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    canvas.fill_rect(0, 9, 34, 3, "soil")
    for y in range(2, 8):
        canvas.paint(6 + y, y, "stone")
        canvas.paint(27 - y, y, "stone")
    canvas.fill_rect(10, 3, 14, 4, "water_light")
    canvas.fill_rect(12, 7, 5, 2, "soil")
    canvas.fill_rect(19, 7, 5, 2, "soil")
    canvas.fill_rect(24, 4, 4, 2, "copper")
    return canvas


def _build_patio_trasero() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "mist")
    canvas.fill_rect(5, 2, 24, 5, "wall")
    _draw_door(canvas, 8, 3, 4, 4)
    _draw_door(canvas, 15, 3, 4, 4)
    _draw_door(canvas, 22, 3, 4, 4)
    canvas.fill_rect(0, 7, 34, 5, "path")
    for x, y in ((6, 9), (12, 10), (18, 9), (24, 10), (29, 9)):
        canvas.paint(x, y, "stone")
    return canvas


def _build_entrada_subterraneo() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 9, 34, 3, "floor")
    canvas.fill_rect(10, 1, 14, 2, "wall")
    canvas.fill_rect(12, 3, 10, 1, "stone")
    canvas.fill_span(4, 13, 20, "stone")
    canvas.fill_span(5, 14, 19, "stone")
    canvas.fill_span(6, 15, 18, "stone")
    canvas.fill_span(7, 16, 17, "stone")
    canvas.fill_rect(15, 8, 4, 1, "night")
    return canvas


def _build_pasillo_piedra() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 9, 34, 3, "floor")
    for y in range(2, 9):
        canvas.paint(6 + y, y, "stone")
        canvas.paint(27 - y, y, "stone")
    canvas.fill_rect(15, 3, 4, 5, "night")
    for x in (10, 23):
        canvas.fill_rect(x, 5, 1, 3, "stone")
    return canvas


def _build_camara_aljibe() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 9, 34, 3, "floor")
    canvas.fill_rect(11, 6, 12, 3, "water")
    canvas.fill_rect(12, 7, 10, 1, "water_light")
    canvas.put_text(7, 6, "O", "stone")
    canvas.put_text(26, 6, "O", "stone")
    canvas.fill_rect(16, 2, 2, 4, "stone")
    return canvas


def _build_gruta_sellada() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 9, 34, 3, "floor")
    canvas.fill_rect(13, 2, 8, 6, "night")
    canvas.fill_rect(16, 3, 1, 4, "stone")
    canvas.fill_rect(21, 7, 4, 1, "stone")
    canvas.fill_rect(22, 8, 2, 1, "stone_dark")
    for x in range(2, 34, 5):
        canvas.paint(x, 10, "stone")
    return canvas


def _build_camara_final() -> PixelCanvas:
    canvas = PixelCanvas(34, 12, "stone_dark")
    canvas.fill_rect(0, 9, 34, 3, "floor")
    _draw_pedestal(canvas, 15, 4)
    canvas.fill_rect(11, 2, 12, 2, "desk")
    canvas.draw_rect(11, 2, 12, 2, "copper")
    canvas.paint(17, 6, "amber")
    return canvas


_SCENE_BUILDERS = {
    "intro_carpeta": _build_intro_folder,
    "camino_entrada": _build_camino_entrada,
    "cruce_bosque": _build_cruce_bosque,
    "sendero_piedras": _build_sendero_piedras,
    "patio_exterior": _build_patio_exterior,
    "vestibulo": _build_vestibulo,
    "exterior_generico": _build_exterior_generico,
    "interior_generico": _build_interior_generico,
    "anexo_generico": _build_anexo_generico,
    "subterraneo_generico": _build_subterraneo_generico,
    "salon_principal": _build_salon_principal,
    "comedor": _build_comedor,
    "cocina": _build_cocina,
    "biblioteca": _build_biblioteca,
    "dormitorio_familiar": _build_dormitorio,
    "cuarto_aperos": _build_cuarto_aperos,
    "capilla_ruinas": _build_capilla_ruinas,
    "sacristia": _build_sacristia,
    "cobertizo": _build_cobertizo,
    "invernadero_abandonado": _build_invernadero,
    "patio_trasero": _build_patio_trasero,
    "entrada_subterraneo": _build_entrada_subterraneo,
    "pasillo_piedra": _build_pasillo_piedra,
    "camara_aljibe": _build_camara_aljibe,
    "gruta_sellada": _build_gruta_sellada,
    "camara_final": _build_camara_final,
}
