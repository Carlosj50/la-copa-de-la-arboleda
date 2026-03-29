from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from game.shared.runtime import resolve_runtime_paths


class RuntimePathsTests(unittest.TestCase):
    def test_source_runtime_paths_point_to_repo_data(self) -> None:
        paths = resolve_runtime_paths()
        self.assertEqual(paths.app_root, PROJECT_ROOT)
        self.assertEqual(paths.bundle_root, PROJECT_ROOT)
        self.assertEqual(paths.world_dir, PROJECT_ROOT / "data" / "world")
        self.assertEqual(paths.save_dir, PROJECT_ROOT / "data" / "saves")

    def test_frozen_runtime_paths_separate_bundle_and_writable_dirs(self) -> None:
        if sys.platform == "win32":
            fake_bundle = Path(r"G:\Temp\_MEI12345")
            fake_executable = Path(r"G:\dist\LaCopaDeLaArboleda.exe")
        else:
            fake_bundle = Path("/tmp/_MEI12345")
            fake_executable = Path("/tmp/dist/LaCopaDeLaArboleda.exe")
        with (
            patch.object(sys, "frozen", True, create=True),
            patch.object(sys, "_MEIPASS", str(fake_bundle), create=True),
            patch.object(sys, "executable", str(fake_executable)),
        ):
            paths = resolve_runtime_paths()

        self.assertEqual(paths.bundle_root, fake_bundle)
        self.assertEqual(paths.app_root, fake_executable.parent)
        self.assertEqual(paths.world_dir, fake_bundle / "data" / "world")
        self.assertEqual(paths.save_dir, fake_executable.parent / "data" / "saves")


if __name__ == "__main__":
    unittest.main()
