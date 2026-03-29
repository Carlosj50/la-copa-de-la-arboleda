"""Retro screen composition helpers."""

from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass

from .text import wrap_for_screen


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
RESET = "\x1b[0m"
DEFAULT_FRAME_WIDTH = 92
DEFAULT_TEXT_WIDTH = 76
DEFAULT_SCENE_HEIGHT = 14
MIN_FRAME_WIDTH = 72
MAX_FRAME_WIDTH = 112
MIN_TEXT_WIDTH = 56
FRAME_STYLE = "38;2;126;110;86"
TITLE_STYLE = "1;38;2;222;206;168"
SUBTITLE_STYLE = "38;2;142;158;128"
SECTION_STYLE = "1;38;2;176;154;114"
FOOTER_STYLE = "38;2;156;156;156"
COMPASS_STYLE = "1;38;2;194;180;144"
COMPASS_GUIDE_STYLE = "38;2;126;110;86"


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def visible_width(value: str) -> int:
    """Return the visible width of *value* without ANSI escapes."""

    return len(ANSI_RE.sub("", value))


def _style(value: str, code: str | None = None) -> str:
    if not code:
        return value
    return f"\x1b[{code}m{value}{RESET}"


def build_compass_lines() -> list[str]:
    """Return a tiny fixed compass rose for visual orientation only."""

    width = 9
    return [
        _pad_visible(_style("N", COMPASS_STYLE), width, "center"),
        _pad_visible(_style("/|\\", COMPASS_GUIDE_STYLE), width, "center"),
        _pad_visible(
            f"{_style('O', COMPASS_STYLE)}{_style('--+--', COMPASS_GUIDE_STYLE)}{_style('E', COMPASS_STYLE)}",
            width,
            "center",
        ),
        _pad_visible(_style('\\|/', COMPASS_GUIDE_STYLE), width, "center"),
        _pad_visible(_style("S", COMPASS_STYLE), width, "center"),
    ]


def horizontal_margin(content_width: int, terminal_width: int | None = None) -> int:
    """Return the left padding needed to center a block of *content_width*."""

    if terminal_width is None:
        terminal_width = shutil.get_terminal_size((DEFAULT_FRAME_WIDTH, 42)).columns
    return max(0, (terminal_width - content_width) // 2)


def center_block(
    text: str,
    *,
    terminal_width: int | None = None,
    terminal_height: int | None = None,
    reserve_lines: int = 0,
) -> str:
    """Center a rendered screen block inside the available terminal space."""

    if not text:
        return text

    if terminal_width is None or terminal_height is None:
        size = shutil.get_terminal_size((DEFAULT_FRAME_WIDTH, 42))
        if terminal_width is None:
            terminal_width = size.columns
        if terminal_height is None:
            terminal_height = size.lines

    lines = text.splitlines()
    max_width = max((visible_width(line) for line in lines), default=0)
    left_padding = horizontal_margin(max_width, terminal_width)
    centered_lines = [
        ((" " * left_padding) + line) if line else ""
        for line in lines
    ]

    content_height = len(centered_lines)
    top_padding = max(0, (terminal_height - content_height - reserve_lines) // 2)
    if top_padding <= 0:
        return "\n".join(centered_lines)
    return ("\n" * top_padding) + "\n".join(centered_lines)


def _pad_visible(value: str, width: int, align: str = "left") -> str:
    diff = max(0, width - visible_width(value))
    if align == "center":
        left = diff // 2
        right = diff - left
        return f"{' ' * left}{value}{' ' * right}"
    if align == "right":
        return f"{' ' * diff}{value}"
    return f"{value}{' ' * diff}"


@dataclass(frozen=True)
class ScreenOptions:
    """Presentation knobs for the console UI."""

    frame_width: int = DEFAULT_FRAME_WIDTH
    text_width: int = DEFAULT_TEXT_WIDTH
    scene_height: int = DEFAULT_SCENE_HEIGHT
    show_scene: bool = True
    compact: bool = False

    @classmethod
    def from_env(cls) -> "ScreenOptions":
        compact = _env_flag("LA_COPA_COMPACT", False)
        show_scene = _env_flag("LA_COPA_VISUAL", True)

        default_frame = 80 if compact else DEFAULT_FRAME_WIDTH
        default_text = 64 if compact else DEFAULT_TEXT_WIDTH
        default_scene_height = 10 if compact else DEFAULT_SCENE_HEIGHT

        try:
            frame_width = int(os.getenv("LA_COPA_SCREEN_WIDTH", str(default_frame)))
        except ValueError:
            frame_width = default_frame
        frame_width = _clamp(frame_width, MIN_FRAME_WIDTH, MAX_FRAME_WIDTH)

        try:
            text_width = int(os.getenv("LA_COPA_TEXT_WIDTH", str(default_text)))
        except ValueError:
            text_width = default_text
        text_width = _clamp(text_width, MIN_TEXT_WIDTH, frame_width - 8)

        return cls(
            frame_width=frame_width,
            text_width=text_width,
            scene_height=default_scene_height if show_scene else 0,
            show_scene=show_scene,
            compact=compact,
        )


class ScreenComposer:
    """Compose stable retro screens for the console runtime."""

    def __init__(self, title: str, options: ScreenOptions | None = None) -> None:
        self.title = title
        self.options = options or ScreenOptions.from_env()

    @property
    def inner_width(self) -> int:
        return self.options.frame_width - 2

    @property
    def text_margin(self) -> int:
        return max(0, (self.inner_width - self.options.text_width) // 2)

    def compose_opening(
        self,
        *,
        scene: str,
        intro_text: str,
        subtitle: str | None,
        footer: str,
    ) -> str:
        body_lines = self._wrap_paragraphs(intro_text)
        return self._compose(
            header=self.title,
            scene=scene,
            title=None,
            subtitle=subtitle,
            result=None,
            body_lines=body_lines,
            detail_lines=[],
            footer=footer,
        )

    def compose_room(
        self,
        *,
        scene: str,
        room_title: str,
        room_subtitle: str | None,
        description: str,
        detail_lines: list[str],
        result: str | None = None,
        footer: str,
    ) -> str:
        return self._compose(
            header=self.title,
            scene=scene,
            title=room_title,
            subtitle=room_subtitle,
            result=result,
            body_lines=self._wrap_paragraphs(description),
            detail_lines=self._wrap_detail_lines(detail_lines),
            footer=footer,
        )

    def compose_message(
        self,
        *,
        scene: str,
        title: str,
        subtitle: str | None,
        body: str,
        footer: str,
    ) -> str:
        return self._compose(
            header=self.title,
            scene=scene,
            title=title,
            subtitle=subtitle,
            result=body,
            body_lines=[],
            detail_lines=[],
            footer=footer,
        )

    def _compose(
        self,
        *,
        header: str,
        scene: str,
        title: str | None,
        subtitle: str | None,
        result: str | None,
        body_lines: list[str],
        detail_lines: list[str],
        footer: str,
    ) -> str:
        frame_lines = [self._top_border()]
        frame_lines.append(
            self._frame_line(_pad_visible(_style(header, TITLE_STYLE), self.inner_width, "center"))
        )
        frame_lines.append(self._divider())

        if self.options.show_scene:
            frame_lines.extend(self._scene_block(scene))
            frame_lines.append(self._divider())

        text_lines: list[str] = []
        if title:
            text_lines.extend(self._text_block([_style(title, TITLE_STYLE)], centered=True))
        if subtitle:
            text_lines.extend(self._text_block([_style(subtitle, SUBTITLE_STYLE)], centered=True))
        if result:
            if text_lines:
                text_lines.append(self._frame_line(" " * self.inner_width))
            text_lines.extend(self._text_block(["Resultado"], label=True))
            text_lines.extend(self._text_block(self._wrap_paragraphs(result)))
        if body_lines:
            if text_lines:
                text_lines.append(self._frame_line(" " * self.inner_width))
            text_lines.extend(self._text_block(body_lines))
        if detail_lines:
            if text_lines:
                text_lines.append(self._frame_line(" " * self.inner_width))
            text_lines.extend(self._text_block(detail_lines))

        frame_lines.extend(text_lines)
        frame_lines.append(self._divider())
        frame_lines.extend(
            self._text_block(self._wrap_paragraphs(footer), centered=True, style=FOOTER_STYLE)
        )
        frame_lines.append(self._bottom_border())
        return "\n".join(frame_lines)

    def _scene_block(self, scene: str) -> list[str]:
        scene_lines = scene.splitlines() if scene else []
        if not scene_lines:
            scene_lines = [" " * 12]
        scene_lines = scene_lines[: self.options.scene_height]
        missing = max(0, self.options.scene_height - len(scene_lines))
        top_padding = missing // 2
        bottom_padding = missing - top_padding
        content_rows = ([""] * top_padding) + scene_lines + ([""] * bottom_padding)

        compass_lines = build_compass_lines()
        compass_width = max((visible_width(line) for line in compass_lines), default=0)
        compass_inset = 2
        gap = 3
        scene_width = max(12, self.inner_width - compass_inset - compass_width - gap)

        rendered_rows: list[str] = []
        for index, line in enumerate(content_rows):
            compass = compass_lines[index] if index < len(compass_lines) else ""
            scene_block = _pad_visible(line, scene_width, "center")
            right_block = _pad_visible(compass, compass_width, "right") + (" " * compass_inset)
            rendered_rows.append(self._frame_line(f"{scene_block}{' ' * gap}{right_block}"))
        return rendered_rows

    def _text_block(
        self,
        lines: list[str],
        *,
        centered: bool = False,
        label: bool = False,
        style: str | None = None,
    ) -> list[str]:
        output: list[str] = []
        for line in lines:
            if not line:
                output.append(self._frame_line(" " * self.inner_width))
                continue
            align = "center" if centered else "left"
            content = _pad_visible(_style(line, style), self.options.text_width, align)
            if label:
                content = _pad_visible(
                    _style(f"[ {line.upper()} ]", SECTION_STYLE),
                    self.options.text_width,
                    "center",
                )
                label = False
            padded = (" " * self.text_margin) + content
            output.append(self._frame_line(_pad_visible(padded, self.inner_width, "left")))
        return output

    def _wrap_paragraphs(self, text: str) -> list[str]:
        return wrap_for_screen(text, width=self.options.text_width).splitlines()

    def _wrap_detail_lines(self, lines: list[str]) -> list[str]:
        output: list[str] = []
        for line in lines:
            wrapped = wrap_for_screen(line, width=self.options.text_width).splitlines()
            output.extend(wrapped or [""])
        return output

    def _top_border(self) -> str:
        return _style(f"┌{'─' * self.inner_width}┐", FRAME_STYLE)

    def _bottom_border(self) -> str:
        return _style(f"└{'─' * self.inner_width}┘", FRAME_STYLE)

    def _divider(self) -> str:
        return _style(f"├{'─' * self.inner_width}┤", FRAME_STYLE)

    def _frame_line(self, content: str) -> str:
        return f"{_style('│', FRAME_STYLE)}{_pad_visible(content, self.inner_width)}{_style('│', FRAME_STYLE)}"
