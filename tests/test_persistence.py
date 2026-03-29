from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from game.content import load_game_definition
from game.persistence import SaveSystem


class SaveSystemTests(unittest.TestCase):
    def test_load_rejects_incompatible_version(self) -> None:
        definition = load_game_definition(PROJECT_ROOT / "data" / "world")
        with tempfile.TemporaryDirectory() as tmp_dir:
            save_path = Path(tmp_dir) / "slot_001.json"
            save_path.write_text(
                json.dumps(
                    {
                        "save_version": definition.data_version + 1,
                        "current_room": definition.start_room,
                    }
                ),
                encoding="utf-8",
            )
            save_system = SaveSystem(save_path)
            with self.assertRaisesRegex(ValueError, "incompatible"):
                save_system.load(definition)

    def test_load_partial_payload_recovers_defaults(self) -> None:
        definition = load_game_definition(PROJECT_ROOT / "data" / "world")
        with tempfile.TemporaryDirectory() as tmp_dir:
            save_path = Path(tmp_dir) / "slot_001.json"
            save_path.write_text(
                json.dumps(
                    {
                        "save_version": definition.data_version,
                        "current_room": definition.start_room,
                        "inventory": ["tabla_suelta"],
                        "flags": {"broken_fence_crossable": True},
                    }
                ),
                encoding="utf-8",
            )
            save_system = SaveSystem(save_path)
            state = save_system.load(definition)
            self.assertEqual(state.current_room_id, definition.start_room)
            self.assertIn("tabla_suelta", state.inventory)
            self.assertEqual(state.object_locations["tabla_suelta"], "__inventory__")
            self.assertFalse(state.object_states["lampara_aceite"]["filled"])
            self.assertTrue(state.flags["broken_fence_crossable"])


if __name__ == "__main__":
    unittest.main()
