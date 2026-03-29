"""Runtime path helpers for source and frozen builds."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    """Resolved paths for bundled assets and writable user data."""

    bundle_root: Path
    app_root: Path
    world_dir: Path
    save_dir: Path


def resolve_runtime_paths() -> RuntimePaths:
    """Return the correct runtime paths for source and PyInstaller builds."""

    if getattr(sys, "frozen", False):
        bundle_root = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        app_root = Path(sys.executable).resolve().parent
    else:
        app_root = Path(__file__).resolve().parents[3]
        bundle_root = app_root

    return RuntimePaths(
        bundle_root=bundle_root,
        app_root=app_root,
        world_dir=bundle_root / "data" / "world",
        save_dir=app_root / "data" / "saves",
    )
