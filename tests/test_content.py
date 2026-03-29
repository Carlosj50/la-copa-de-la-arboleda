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


def read_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_world_fixture(
    target: Path,
    *,
    world: object,
    rooms: object,
    objects: object,
    interactions: object,
) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name, payload in {
        "world.json": world,
        "rooms.json": rooms,
        "objects.json": objects,
        "interactions.json": interactions,
    }.items():
        with (target / name).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)


class ContentTests(unittest.TestCase):
    def test_world_definition_loads(self) -> None:
        definition = load_game_definition(Path("data/world"))
        self.assertEqual(definition.title, "La Copa de la Arboleda")
        self.assertEqual(len(definition.rooms), 24)
        self.assertGreaterEqual(len(definition.objects), 40)
        self.assertGreaterEqual(len(definition.interactions), 15)
        self.assertIn(definition.start_room, definition.rooms)

    def test_key_rooms_and_flags_exist(self) -> None:
        definition = load_game_definition(Path("data/world"))
        self.assertIn("capilla_ruinas", definition.rooms)
        self.assertIn("copa_plata", definition.objects)
        self.assertIn("broken_fence_crossable", definition.initial_flags)
        self.assertIn("grotto_open", definition.initial_flags)
        self.assertEqual(definition.intro_scene, "intro_carpeta")
        self.assertEqual(definition.rooms["camino_entrada"].scene_id, "camino_entrada")
        self.assertEqual(definition.rooms["salon_principal"].scene_id, "salon_principal")
        self.assertEqual(definition.rooms["biblioteca"].scene_id, "biblioteca")
        self.assertEqual(definition.rooms["entrada_subterraneo"].scene_id, "entrada_subterraneo")
        self.assertEqual(definition.rooms["capilla_ruinas"].scene_id, "capilla_ruinas")
        self.assertEqual(definition.rooms["pasillo_piedra"].scene_id, "pasillo_piedra")
        self.assertEqual(definition.rooms["camara_final"].scene_id, "camara_final")

    def test_fixture_kind_and_room_alias_discipline(self) -> None:
        definition = load_game_definition(Path("data/world"))
        self.assertEqual(definition.objects["roseton_capilla"].kind, "fixture")
        self.assertNotIn("pozo", definition.rooms["claro_pozo_seco"].aliases)
        self.assertNotIn("verja", definition.rooms["sendero_piedras"].aliases)

    def test_invalid_local_alias_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = PROJECT_ROOT / "data" / "world"
            world = read_json(base / "world.json")
            rooms = read_json(base / "rooms.json")
            objects = read_json(base / "objects.json")
            interactions = read_json(base / "interactions.json")

            for room in rooms:
                if room["id"] == "claro_pozo_seco":
                    room["aliases"].append("pozo")
                    break

            write_world_fixture(
                Path(tmp_dir),
                world=world,
                rooms=rooms,
                objects=objects,
                interactions=interactions,
            )

            with self.assertRaisesRegex(ValueError, "colliding"):
                load_game_definition(Path(tmp_dir))

    def test_unsupported_condition_type_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = PROJECT_ROOT / "data" / "world"
            world = read_json(base / "world.json")
            rooms = read_json(base / "rooms.json")
            objects = read_json(base / "objects.json")
            interactions = read_json(base / "interactions.json")

            rooms[0]["exits"]["ESTE"]["conditions"] = [{"type": "moon_phase", "name": "full"}]

            write_world_fixture(
                Path(tmp_dir),
                world=world,
                rooms=rooms,
                objects=objects,
                interactions=interactions,
            )

            with self.assertRaisesRegex(ValueError, "unsupported condition type"):
                load_game_definition(Path(tmp_dir))

    def test_unknown_room_scene_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            base = PROJECT_ROOT / "data" / "world"
            world = read_json(base / "world.json")
            rooms = read_json(base / "rooms.json")
            objects = read_json(base / "objects.json")
            interactions = read_json(base / "interactions.json")

            for room in rooms:
                if room["id"] == "camino_entrada":
                    room["scene"] = "escena_fantasma"
                    break

            write_world_fixture(
                Path(tmp_dir),
                world=world,
                rooms=rooms,
                objects=objects,
                interactions=interactions,
            )

            with self.assertRaisesRegex(ValueError, "unknown scene"):
                load_game_definition(Path(tmp_dir))


if __name__ == "__main__":
    unittest.main()
