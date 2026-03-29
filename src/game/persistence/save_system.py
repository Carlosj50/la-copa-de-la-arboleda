"""JSON save/load helpers."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from game.model import GameDefinition, GameState


class SaveSystem:
    """Persist and restore a game state from JSON."""

    def __init__(self, save_path: Path) -> None:
        self._save_path = save_path

    def save(self, definition: GameDefinition, state: GameState) -> None:
        self._save_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "save_version": definition.data_version,
            "current_room": state.current_room_id,
            "inventory": state.inventory,
            "flags": state.flags,
            "object_locations": state.object_locations,
            "object_states": state.object_states,
            "visited_rooms": sorted(state.visited_rooms),
        }
        with self._save_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

    def exists(self) -> bool:
        return self._save_path.exists()

    def load(self, definition: GameDefinition) -> GameState:
        with self._save_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        save_version = payload.get("save_version")
        if save_version != definition.data_version:
            raise ValueError(
                f"El save es incompatible con la versión de datos actual ({save_version} != {definition.data_version})."
            )

        current_room = payload["current_room"]
        if current_room not in definition.rooms:
            raise ValueError(f"El save apunta a una habitación desconocida: {current_room}")

        inventory = list(payload.get("inventory", []))
        unknown_inventory = [object_id for object_id in inventory if object_id not in definition.objects]
        if unknown_inventory:
            unknown_text = ", ".join(sorted(unknown_inventory))
            raise ValueError(f"El save contiene objetos desconocidos en inventario: {unknown_text}")

        flags = deepcopy(definition.initial_flags)
        payload_flags = dict(payload.get("flags", {}))
        unknown_flags = sorted(set(payload_flags) - set(definition.initial_flags))
        if unknown_flags:
            unknown_text = ", ".join(unknown_flags)
            raise ValueError(f"El save contiene flags desconocidas: {unknown_text}")
        flags.update(payload_flags)

        object_locations = {
            object_id: object_definition.location
            for object_id, object_definition in definition.objects.items()
        }
        payload_locations = dict(payload.get("object_locations", {}))
        for object_id, location in payload_locations.items():
            if object_id not in definition.objects:
                raise ValueError(f"El save contiene ubicación para objeto desconocido: {object_id}")
            if location not in definition.rooms and location not in {"__inventory__", "__nowhere__"}:
                raise ValueError(f"El save contiene una ubicación inválida para {object_id}: {location}")
            object_locations[object_id] = location

        object_states = {
            object_id: {"visible": object_definition.initial_visible, **deepcopy(object_definition.initial_states)}
            for object_id, object_definition in definition.objects.items()
        }
        payload_states = dict(payload.get("object_states", {}))
        for object_id, state_payload in payload_states.items():
            if object_id not in definition.objects:
                raise ValueError(f"El save contiene estado para objeto desconocido: {object_id}")
            object_states[object_id].update(deepcopy(state_payload))

        for object_id in inventory:
            object_locations[object_id] = "__inventory__"
        for object_id, location in object_locations.items():
            if location == "__inventory__" and object_id not in inventory:
                inventory.append(object_id)

        visited_rooms = set(payload.get("visited_rooms", []))
        unknown_visited = sorted(room_id for room_id in visited_rooms if room_id not in definition.rooms)
        if unknown_visited:
            unknown_text = ", ".join(unknown_visited)
            raise ValueError(f"El save contiene habitaciones visitadas desconocidas: {unknown_text}")

        return GameState(
            current_room_id=current_room,
            inventory=inventory,
            flags=flags,
            object_locations=object_locations,
            object_states=object_states,
            visited_rooms=visited_rooms,
        )
