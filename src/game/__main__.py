"""Console entry point."""

from __future__ import annotations

import os
import shutil
import sys
import time

from game.engine import GameSession
from game.shared.pixel_art import enable_console_ansi
from game.shared.runtime import resolve_runtime_paths
from game.shared.screen import center_block, horizontal_margin


def clear_screen() -> None:
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def print_centered_screen(
    text: str,
    reserve_lines: int = 2,
    *,
    terminal_width: int | None = None,
    terminal_height: int | None = None,
) -> None:
    print(
        center_block(
            text,
            reserve_lines=reserve_lines,
            terminal_width=terminal_width,
            terminal_height=terminal_height,
        )
    )


def wait_for_terminal_layout(
    content_width: int,
    *,
    minimum_height: int = 24,
    attempts: int = 8,
    delay: float = 0.05,
) -> os.terminal_size:
    last_size: tuple[int, int] | None = None
    stable_hits = 0
    for _ in range(attempts):
        size = shutil.get_terminal_size((content_width, minimum_height))
        current = (size.columns, size.lines)
        if current[0] >= content_width and current[1] >= minimum_height:
            if current == last_size:
                stable_hits += 1
                if stable_hits >= 1:
                    return size
            else:
                stable_hits = 0
        last_size = current
        time.sleep(delay)
    return shutil.get_terminal_size((content_width, minimum_height))


def main() -> int:
    enable_console_ansi()
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    runtime_paths = resolve_runtime_paths()
    session = GameSession.from_runtime_paths(runtime_paths)
    startup_size = wait_for_terminal_layout(session.screen.options.frame_width, minimum_height=32)
    clear_screen()
    print_centered_screen(
        session.opening_text(),
        terminal_width=startup_size.columns,
        terminal_height=startup_size.lines,
    )

    intro_margin = " " * horizontal_margin(
        session.screen.options.frame_width,
        startup_size.columns,
    )
    try:
        input(f"\n{intro_margin}Pulsa INTRO para entrar en La Arboleda...")
    except EOFError:
        print("\nHasta pronto.")
        return 0

    clear_screen()
    print_centered_screen(session.render_room_screen(force_full=True))

    while not session.state.exit_requested and not session.state.game_over:
        prompt_margin = " " * horizontal_margin(session.screen.options.frame_width)
        try:
            raw_command = input(f"\n{prompt_margin}Acción > ")
        except EOFError:
            print("\nHasta pronto.")
            return 0
        response = session.execute(raw_command, as_screen=True)
        if response:
            clear_screen()
            print_centered_screen(response)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
